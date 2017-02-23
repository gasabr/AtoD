#!/usr/bin/env python3
import unittest
import json

from atod.tools.game_files import to_json

EXAMPLES_FOLDER = '/Users/gasabr/AtoD/atod/tests/tests_data/game_files/'


class TestParser(unittest.TestCase):
    ''' Test case for game files parser.

        In examples are small files with all hard cases I've ran into,
        expected_*.json represents result what is expected from parser.
    '''
    def test_comments(self):
        ''' Tests every case of placing comments in file. '''
        # BUG: handle space in ItemAliases.
        #      now if there's space in alias it will be removed
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

    #
    # def test_clearly_defined_float(self):
    #     # BUG: there was only one value 0.036f in items, there is a need to
    #     #      handle it.
    #     self.assertEqual(1, 0)


if __name__ == '__main__':
    unittest.main()
