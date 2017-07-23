#!/usr/bin/env python3
import unittest

from atod import Heroes

class TestHeroes(unittest.TestCase):

    def setUp(self):
        self.heroes_from_ids = Heroes.from_ids([1, 14, 112])
        self.heroes_from_names = Heroes(['Sniper', 'Lina', 'Dazzle'])

    def test_init_with_ids(self):
        ''' I'm not sure how to test classes like this.

        So, what tests are doing is basically: call method with some arguments,
        check if something goes wrong.

        '''
        # this is fine
        Heroes.from_ids([1, 14, 112])

        # call with invalid id
        self.assertRaises(ValueError, Heroes.from_ids, [0, 228])

        # call with non-integer id
        self.assertRaises(TypeError, Heroes.from_ids, ['1', 54])

        # call with specific patch, fine too
        Heroes.from_ids([15, 25, 89], patch='706')

       
    def test_init_with_names(self):
        ''' I'm not sure how to test classes like this.

        So, what tests are doing is basically: call method with some arguments,
        check if something goes wrong.

        '''
        # this is fine
        Heroes.from_names(['Gyrocopter', 'Bounty Hunter', 'Viper'])

        # call with invalid id
        self.assertRaises(ValueError, Heroes.from_names, ['Best hero', 'Anti-Mage'])

        # call with non-string id
        self.assertRaises(TypeError, Heroes.from_ids, ['Shadow Fiend', 54])

        # call with specific patch, fine too
        Heroes.from_names(['Axe', 'Underlord', 'Bane'], patch='706')


    def test_iter(self):
        ''' One more time:

        I'm not sure what to do there, but user should be able to iterate over
        heroes.
        '''

        for hero in self.heroes_from_ids:
            pass
