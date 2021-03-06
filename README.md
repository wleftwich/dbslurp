# Dump SQL database to JSON files
`sql2json.py` will serialize an SQL database to JSON.
 Each table occupies a directory, each row a file.

## Installation
The script has been tested with Python 2.7.
Requires http://sqlalchemy.org plus whatever database adapter is applicable.

## Usage
`$ python sql2json.py settings.json`

## Configuration
The script expects a JSON file containing configuration.
Example:

    {
        "connect": "mysql+mysqldb://aviationweek:aviationweek@localhost/aviationweek?charset=utf8",
        "output_folder": "dump",
        "encoding": "utf8",
        "include_tables": [],
        "exclude_tables": [],
        "views_too": false,
        "max_rows": 10
    }

- *connect*: sqlalchemy connection string. *Required* -- all other keys have defaults.
- *output_folder*: defaults to "dump"
- *encoding*: "encoding" param for json.dump(), only used if db adapter does not return unicode. Default "utf8"
- *include_tables*: defaults to empty list, which means "all"
- *exclude_tables*: tables to ignore, overriding "include_tables". Defaults to empty list.
- *views_too*: also export database views
- *max_rows*: how many rows to export from each table. Defaults to 0, which means "all"

## Primary keys and filenames
If the table has a primary key, each row's filename will be derived from it. (Multiple column keys OK.)

Otherwise, each row's filename will be a UUID.

## JSON serialization defaults
If json.dump() does not know how to handle a value in a database row, it will first attempt to apply float(). If that fails, it will apply repr().


# List tables, counts, keys
`sqlinfo.py` will print a tab-separated report showing table names, counts, primary keys, foreign keys

## Usage
`$ python sqlinfo.py settings.json > outputfilename.tsv`


## Configuration
Uses the same json config file as sql2json.py, though only the 'connect' field is used.









