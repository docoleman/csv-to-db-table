# DB table generator based on CSV file #
Read a CSV file and output a DDL script that will define a table matching the
file. It will allow you to quickly and easily load a file that matches that
specification into a table created using the output DDL script.

## Description ##

Generate a create table statement based off of a CSV file. The header names
will be the contents of the columns in the first row of the file, the
table name is specified on the command line.
Types will be inferred, if there is data in the columns, otherwise, they will
all be VARCHAR(256).
Table names will be validated for compliance with SQL naming standards. SQL
reserved keywords will be rejected as table names.

## Usage ##
usage: csv\_to\_db\_file [-h] [-x  [...]] [-r  [...]] table [FILE]

convert a CSV file to database table definition

positional arguments:
  table                 Table name for output
  FILE                  with no FILE, or when FILE is -, read standard input

optional arguments:
  -h, --help            show this help message and exit
  -x  [ ...], --exclude-columns  [ ...]
                        list of columns to exclude from output
  -r  [ ...], --reserved-word  [ ...]
                        list of files containing reserved words

table names will be rejected for failing to conform to SQL standards. Reserved
keywords, etc.

