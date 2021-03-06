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
        table_name = ("ThisNameIsWayTooLongIfItWasShorterItWouldBeValidButIt"
                "IsTooLongSoItIsNotValid")
        expected = ("ThisNameIsWayTooLongIfItWasShorterItWouldBeValidButItIs"
                "TooLongSoItIsNotValid is too long. Please use 64 or fewer"
                " characters")
        actual = self.csvToDbTable.valid_table_name(
            table_name,
            ['bad_name', 'invalid_name']
        )
        self.assertFalse(actual['valid'])
        self.assertEqual(expected, actual['message'])


    def test_valid_table_name_spaces(self):
        expected = ("Table name cannot contain whitespace. Please remove "
                "whitespace from bad name")
        actual = self.csvToDbTable.valid_table_name(
            'bad name', ['bad_name', 'invalid_name']
        )
        self.assertFalse(actual['valid'])
        self.assertEqual(expected, actual['message'])


    def test_format_column_upper(self):
        self.assertEqual("upper", self.csvToDbTable.format_column("UPPER"))


    def test_format_column_no_change(self):
        self.assertEqual("no-change", self.csvToDbTable.format_column("no-change"))


    def test_format_column_empty_string(self):
        self.assertEqual("", self.csvToDbTable.format_column(""))


    def test_format_column_spaces(self):
        self.assertEqual("s_paces", self.csvToDbTable.format_column("s paces"))


    def test_format_column_max_length(self):
        name = ("thisnameiswaytoolongifitwasshorteritwouldbevalidbutit"
                "istoolongsoitwillbeshortened")
        expected = ("thisnameiswaytoolongifitwasshorteritwouldbevalidbutitis"
                "toolongso")
        self.assertEqual(expected, self.csvToDbTable.format_column(name))


if __name__ == "__main__":
    unittest.main()
