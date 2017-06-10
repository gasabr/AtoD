#!/usr/bin/env python3
import unittest
from pprint import pprint

from atod.heroes import Hero, camel2python
from atod.heroes_graph import add_weight


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

    def test_add_weight(self):
        C = [[0 for x in range(6)] for y in range(6)]
        pprint(C)

        winner = [1, 2, 3]
        looser = [5, 2, 4]

        add_weight(C, winner, 0.2)
        pprint(C)


if __name__ == '__main__':
    unittest.main()
