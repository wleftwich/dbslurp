#!/usr/bin/env python
"""db2json.py
Dump an SQL database to JSON files.
Tested with Python 2.7
Requires sqlalchemy and relevant database library
"""

import sys
import os
import json
import uuid
import sqlalchemy as sa

defaults = {
    'connect': None, # sqlalchemy connect string required
    'output_folder': 'dump',
    'encoding': 'utf8',  # encoding param for json.dump()
    'max_rows': 0,  # 0 => all rows for each table
    'include_tables': [], # empty list => all
    'exclude_tables': [], # overrides 'include_tables'
    'views_too': False  # also export database views
}


def jsondefault(obj):
    """Handle datetime objects and any unknown type that can be an argument for float().
    Otherwise, if an object cannot be serialized to json, return its repr().
    """
    try:
        return obj.isoformat()
    except:
        pass

    try:
        return float(obj)
    except:
        return repr(obj)


def dbconnect(connect_str):
    engine = sa.create_engine(connect_str)
    meta = sa.MetaData(bind=engine)
    return meta


def export_table(table,
                 outbox=defaults['output_folder'],
                 max_rows=defaults['max_rows'],
                 encoding=defaults['encoding']):
    folder = os.path.join(outbox, table.key)
    if not os.path.exists(folder):
        os.makedirs(folder)
    pk = table.primary_key
    if pk:
        keys = pk.columns.keys()
    else:
        keys = None
    rows = sa.select([table]).execute()
    for i, row in enumerate(rows):
        if max_rows and i >= max_rows:
            break
        try:
            copy_row(row, keys, folder, encoding)
        except:
            sys.stderr.write(repr(table).encode('utf8') + '\n\n' + repr(row).encode('utf8') + '\n\n')
            raise


def copy_row(row, keys, folder, encoding=defaults['encoding']):
    if keys:
        fn = ('-'.join(unicode(row[k]).replace('/', '--') for k in keys) + '.json').encode('ascii', 'ignore')
    else:
        fn = str(uuid.uuid4()) + '.json'
    fqfn = os.path.join(folder, fn)
    with open(fqfn, 'w') as fh:
        json.dump(dict(row), fh, indent=2, default=jsondefault, encoding=encoding)


def main(settings):
    config = defaults.copy()
    config.update(settings)
    meta = dbconnect(settings['connect'])
    meta.reflect(views=config['views_too'])

    if config['include_tables']:
        tables = (meta.tables[x] for x in config['include_tables']
                    if x not in config['exclude_tables'])
    else:
        tables = (x for x in meta.sorted_tables
                    if x.key not in config['exclude_tables'])

    for table in tables:
        export_table(table,
                     outbox=config['output_folder'],
                     max_rows=config['max_rows'],
                     encoding=config['encoding'])


if __name__ == '__main__':
    settings_file = sys.argv[1]
    with open(settings_file) as fh:
        settings = json.load(fh)
    main(settings)











