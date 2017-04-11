#!/usr/bin/env python3
import unittest

from atod.heroes import Hero

class TestHero(unittest.TestCase):

    def setUp(self):
        self.sf_1 = Hero('Shadow Fiend')
        self.sf_10 = Hero('Shadow Fiend', 10)

    def test_id(self):
        self.assertEqual(self.sf_1.id, 11)

    def test_lvl(self):
        self.assertEqual(self.sf_10.lvl, 10)

    def test_in_game_name(self):
        self.assertEqual(self.sf_1.in_game_name, 'nevermore')

    def test_abilities_adding(self):
        self.assertEqual(len(self.sf_1.abilities), 6)


if __name__ == '__main__':
    unittest.main()
