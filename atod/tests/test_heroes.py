#!/usr/bin/env python3
import unittest

from atod import Hero, Heroes

class TestHeroes(unittest.TestCase):

    def setUp(self):
        self.all_heroes = Heroes.all()

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

        heroes = Heroes.from_ids([1, 15, 65])

        for hero in heroes:
            pass

    def test_get_ids(self):
        names = ['Sniper', 'Lina', 'Dazzle']
        heroes = Heroes.from_names(names)
        ids = heroes.get_ids()

        for name in names:
            self.assertEqual(ids[name], Hero.from_name(name).id)

        bin_ids = heroes.get_ids(binarised=True)
        # len of binarised ids should be equal to amount of heroes
        self.assertEqual((len(self.all_heroes),), bin_ids.shape)
        # amount of 1s should be equal to amount of heroes in the object
        self.assertEqual(len(list(filter(lambda x: x==1, bin_ids))),
                         len(heroes))
