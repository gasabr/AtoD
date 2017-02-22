#!/usr/bin/env python3
import unittest
import json

from atod.hero import Hero
from atod.tools.game_files import to_json

EXAMPLES_FOLDER = '/Users/gasabr/AtoD/atod/tests/tests_data/game_files/'

class TestHero(unittest.TestCase):
    def test_creation_by_name(self):
        self.es_1 = Hero('Axe')
        self.assertEqual(self.es_1.id, 2)

    def test_creation_with_lvl(self):
        self.es_10 = Hero('Axe', 10)
        self.assertEqual(self.es_10.id, 2)


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

        self.assertEqual(expected, parsed)

    def test_delimeters(self):
        ''' Tests ways to separate strings, keys, values. '''
        input_file = EXAMPLES_FOLDER + 'delimeters.txt'
        parsed = to_json(input_file)

        with open(EXAMPLES_FOLDER + 'expected_delimeters.json', 'r') as fp:
            expected = json.load(fp)

        self.assertEqual(expected, parsed)

    def test_indents(self):
        ''' Tests ways to separate strings, keys, values. '''
        input_file = EXAMPLES_FOLDER + 'intends.txt'
        parsed = to_json(input_file)

        with open(EXAMPLES_FOLDER + 'expected_intends.json', 'r') as fp:
            expected = json.load(fp)

        self.assertEqual(expected, parsed)

    def test_clearly_defined_float(self):
        # BUG: there was only one value 0.036f in items, there is a need to
        #      handle it.
        self.assertEqual(1, 0)


class TestSettings(unittest.TestCase):
    ''' Tests existence of all files, converter. '''
    pass


if __name__ == '__main__':
    unittest.main()
