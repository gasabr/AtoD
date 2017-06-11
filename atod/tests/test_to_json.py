#!/usr/bin/env python3
import json
import unittest

from atod.utils.txt2json import to_json, _clean_value

EXAMPLES_FOLDER = '/Users/gasabr/AtoD/atod/tests/tests_data/game_files/'


class TestParser(unittest.TestCase):
    ''' Test case for game files parser.

        In examples/ there are small files with all hard cases I've ran into,
        expected_*.json represents result what is expected from parser.
    '''
    def test_comments(self):
        ''' Tests every case of placing comments in file. '''
        input_file = EXAMPLES_FOLDER + 'comments.txt'
        parsed = to_json(input_filename=input_file)

        with open(EXAMPLES_FOLDER + 'expected_comments.json', 'r') as fp:
            expected = json.load(fp)

        # I don't now why, but sorted is required here
        self.assertEqual(sorted(expected), sorted(parsed))

    def test_delimeters(self):
        ''' Tests ways to separate strings, keys, values. '''
        input_file = EXAMPLES_FOLDER + 'delimeters.txt'
        parsed = to_json(input_file)

        with open(EXAMPLES_FOLDER + 'expected_delimeters.json', 'r') as fp:
            expected = json.load(fp)

        self.assertEqual(sorted(expected), sorted(parsed))

    def test_indents(self):
        ''' Tests ways to separate strings, keys, values. '''
        input_file = EXAMPLES_FOLDER + 'intends.txt'
        parsed = to_json(input_file)

        with open(EXAMPLES_FOLDER + 'expected_intends.json', 'r') as fp:
            expected = json.load(fp)

        self.assertEqual(sorted(expected), sorted(parsed))

    def test_float_fields(self):
        ''' Example with float fields. '''
        input_file = EXAMPLES_FOLDER + 'float_fields.txt'
        parsed = to_json(input_file)

        with open(EXAMPLES_FOLDER + 'expected_float_fields.json', 'r') as fp:
            expected = json.load(fp)

        self.assertEqual(sorted(parsed), sorted(expected))

    def test_empty_value(self):
        ''' Example with empty value in the input file. '''
        input_file = EXAMPLES_FOLDER + 'empty_values.txt'
        parsed = to_json(input_file)

        with open(EXAMPLES_FOLDER + 'expected_empty_values.json', 'r') as fp:
            expected = json.load(fp)

        self.assertEqual(sorted(parsed), sorted(expected))

    def test_empty_dict(self):
        ''' Example with empty dictionary in the input file. '''
        input_file = EXAMPLES_FOLDER + 'empty_dict.txt'
        parsed = to_json(input_file)

        with open(EXAMPLES_FOLDER + 'expected_empty_dict.json', 'r') as fp:
            expected = json.load(fp)

        # sorted removes empty dictionaries
        self.assertEqual(sorted(parsed), sorted(expected))

    def test_symbols_in_values(self):
        ''' Test different unusual symbols in values. '''
        input_file = EXAMPLES_FOLDER + 'symbols_in_values.txt'
        parsed = to_json(input_file)

        with open(EXAMPLES_FOLDER + 'expected_symbols_in_values.json', 'r') as fp:
            expected = json.load(fp)

        self.assertEqual(sorted(parsed), sorted(expected))

    def test_numbers_parsing(self):
        ''' Tests how numbers inside of "" can be converted to their values. '''
        input_file = EXAMPLES_FOLDER + 'numbers.json'

        with open(input_file, 'r') as fp:
            data = json.load(fp)

        for example in data:
            self.assertEqual(_clean_value(example['input']), example['output'])


if __name__ == '__main__':
    unittest.main()
