from argparse import ArgumentParser,FileType as ArgParseFileType
from sys import stdin, stderr, exit as sysexit
import csv
import re

class CsvToDbTable:
    '''
    Generate a create table statement based off of a CSV file. The header names \
            will be the contents of the columns in the first row of the file, the \
            table name is specified on the command line.
    Types will be inferred, if there is data in the columns, otherwise, they will \
            all be VARCHAR(256).
    Table names will be validated for compliance with SQL naming standards. SQL \
            reserved keywords will be rejected as table names.
    '''


    def __init__(self,
            arg_parser=None,
            preamble_format="CREATE TABLE {0} (\n  ",
            conclusion="\n);",
            table_name=None,
            default_type="NVARCHAR(512)",
            separator=",\n  ",
            max_name_length=64
    ):
        self.arg_parser = self.init_args(arg_parser)
        self.preamble_format = preamble_format
        self.conclusion = conclusion
        self.table_name = None
        self.default_type = default_type
        self.separator = separator
        self.max_name_length = max_name_length


    def error_message(self, message=""):
        if message:
            print(message, file=stderr)
        self.arg_parser.print_help()


    def init_args(self, arg_parser=None):
        parser = arg_parser if arg_parser else ArgumentParser(prog="csv_to_db_file",
                description="convert a CSV file to database table definition",
                epilog="table names will be rejected for failing to conform to SQL \
                        standards. Reserved keywords, etc.")
        parser.add_argument("table", help="Table name for output")
        parser.add_argument("file", metavar="FILE", nargs="?",
                help="with no FILE, or when FILE is -, read standard input",
                type=ArgParseFileType('r'), default=stdin)
        parser.add_argument("-x", "--exclude-columns", nargs="+", metavar="",
                help="list of columns to exclude from output")
        parser.add_argument("-r", "--reserved-word", nargs="+", metavar="",
                help="list of files containing reserved words")

        return parser


    def reserved_words(self, base="/home/darcy/Dev/csv-to-db-table/resources/pg_sql_keywords.txt", extra=None):
        with open(base, "r") as keywords_file:
            keywords = keywords_file.read().splitlines()

        if not keywords:
            return False

        return keywords


    def valid_table_name(self, table_name, banned_words=None):
        # Table name may not contain any spaces
        if re.search(r"\s", table_name):
            message = ("Table name cannot contain whitespace. Please remove "
                    "whitespace from {0}").format(table_name)
            return {'valid':False, 'message':message}

        # 64 is a magic number for object name length in some SQL implementations
        # It is used as the default max_name_length. If a different length is
        # required, it can be configured on the command line
        if len(table_name) > self.max_name_length:
            message = ("{0} is too long. Please use {1} or fewer characters"
                    ).format(table_name, self.max_name_length)
            return {'valid':False, 'message':message}

        # List of banned words that will cause object naming to fail
        if table_name in banned_words:
            message = "{0} is a reserved keyword".format(table_name)
            return {'valid':False, 'message':message}

        return {'valid':True, 'message':""}


    def list_columns(self, input_file):
        columns = []

        with input_file as csv_file:
            csv_reader = csv.reader(csv_file)

            try:
                header = next(csv_reader)
            except StopIteration:
                return False

            columns = [{'name':self.format_column(x), 'type':self.default_type}
                    for x in header]

        return columns


    def format_column(self, column):
        fixed_column = column.lower()
        fixed_column = fixed_column.replace(" ", "_")
        fixed_column = fixed_column[:self.max_name_length]
        return fixed_column


    def main(self):
        args = self.arg_parser.parse_args()
        table_name = args.table
        keywords = self.reserved_words()
        summary = self.valid_table_name(table_name, keywords)
        if not summary['valid']:
            self.error_message(summary.message)
            return False

        column_list = self.list_columns(args.file)
        if not column_list:
            self.error_message("No columns found in CSV file {0}".format(args.file.name))
            return False

        create_statement = self.preamble_format.format(table_name)
        create_statement += self.separator.join([x['name'] + " " + x['type'] for x in column_list])
        create_statement += self.conclusion if self.conclusion else ""

        print(create_statement)


if __name__ == "__main__":
    table = CsvToDbTable()
    table.main()
