#!/usr/bin/env python3
import unittest

from atod.models.heroes import Hero, camel2python


class TestHero(unittest.TestCase):

    def setUp(self):
        self.sf_1 = Hero(11)
        self.sf_10 = Hero(11, 10)

    def test_id(self):
        self.assertEqual(self.sf_1.id, 11)

    def test_lvl(self):
        self.assertEqual(self.sf_10.lvl, 10)

    def test_in_game_name(self):
        self.assertEqual(self.sf_1.in_game_name, 'nevermore')

    def test_abilities_adding(self):
        self.assertEqual(len(self.sf_1.abilities), 6)

    def test_camel2python(self):
        test_str = 'PrimaryAttribute'
        self.assertEqual(camel2python(test_str), 'primary_attribute')


if __name__ == '__main__':
    unittest.main()
