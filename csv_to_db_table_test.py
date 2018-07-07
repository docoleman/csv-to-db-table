import unittest
from unittest.mock import Mock
import argparse
import csv_to_db_table

## Test csv_to_db_table
## Two fixtures available
##  test0.csv
##  test_empty.csv

class TestCsvToDbTable(unittest.TestCase):
    def setUp(self):
        argParser = Mock(argparse.ArgumentParser)
        self.csvToDbTable=csv_to_db_table.CsvToDbTable(argParser)


    def test_valid_table_name_valid(self):
        self.assertTrue(self.csvToDbTable.valid_table_name(
            'good_name', ['bad_name', 'invalid_name']
        )['valid'])


    def test_valid_table_name_in_banned_list(self):
        self.assertFalse(self.csvToDbTable.valid_table_name(
            'bad_name', ['bad_name', 'invalid_name']
        )['valid'])


    def test_valid_table_name_too_long(self):
        self.assertFalse(self.csvToDbTable.valid_table_name(
            'bad_name', ['bad_name', 'invalid_name']
        )['valid'])


    def test_valid_table_name_spaces(self):
        expected = ("Table name cannot contain whitespace. Please remove "
                "whitespace from bad name")
        valid_result = self.csvToDbTable.valid_table_name(
            'bad name', ['bad_name', 'invalid_name']
        )
        self.assertFalse(valid_result['valid'])
        self.assertEqual(expected, valid_result['message'])


if __name__ == "__main__":
    unittest.main()
