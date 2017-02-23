#!/usr/bin/env python3
import unittest

from atod.hero import Hero

class TestHero(unittest.TestCase):
    def test_creation_by_name(self):
        self.es_1 = Hero('Axe')
        self.assertEqual(self.es_1.id, 2)

    def test_creation_with_lvl(self):
        self.es_10 = Hero('Axe', 10)
        self.assertEqual(self.es_10.id, 2)


if __name__ == '__main__':
    unittest.main()
