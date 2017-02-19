#!/usr/bin/env python3
import unittest

from hero import Hero

class TestHero(unittest.TestCase):
    def test_creation_by_name(self):
        self.es_1 = Hero('Earthshaker')

    def test_creation_with_lvl(self):
        self.es_10 = Hero('Earthshaker', 10)


if __name__ == '__main__':
    unittest.main()
