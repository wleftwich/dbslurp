#!/usr/bin/env python
"""sqlinfo.py
Summary info for SQL database
Tested with Python 2.7
Requires sqlalchemy and relevant database library
"""

USAGE = 'Usage: python sqlinfo.py settings.json'

import sys
import json
import sqlalchemy as sa

def dbconnect(connect_str):
    engine = sa.create_engine(connect_str)
    meta = sa.MetaData(bind=engine)
    return meta


def table_info(tbl):
    count = tbl.count().execute().fetchall()[0][0]

    primary = tbl.primary_key
    if primary:
        pk = primary.columns.keys()
    else:
        pk = []
    fks = sorted(set(str(fk.column) for fk in tbl.foreign_keys))
    
    return {'name': tbl.fullname,
            'count': count,
            'pk': pk,
            'fks': fks}
    

def list_table_info(tbls):
    return (table_info(tbl) for tbl in tbls)
    

def main(settings):
    meta = dbconnect(settings['connect'])
    meta.reflect()
    print 'table\tcount\tprimary_key\tforeign_keys'
    for info in list_table_info(meta.sorted_tables):
        rec = (info['name'],
               str(info['count']),
               ','.join(info['pk']),
               ','.join(info['fks'])
            )
        print '\t'.join(rec)        


if __name__ == '__main__':
    try:
        settings_file = sys.argv[1]
    except IndexError:
        print USAGE
        exit(1)
    if settings_file in ('-h', '--help'):
        print USAGE
        exit(0)
    with open(settings_file) as fh:
        settings = json.load(fh)
    main(settings)

