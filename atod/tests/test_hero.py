#!/usr/bin/env python3
import unittest

from atod.models.hero import camel2python
from atod import Hero


class TestHero(unittest.TestCase):

    def setUp(self):
        ''' Creates 2 Shadow Fiends to test methods. '''
        self.sf_1 = Hero(11)
        self.sf_10 = Hero(11, 10)

    def test_init(self):
        ''' Tests different ways to create hero. '''
        # default init function takes id (int), lvl (int), patch(str)
        # there are examples of wrong usage
        self.assertRaises(TypeError, Hero, 'Earthshaker')
        self.assertRaises(TypeError, Hero, 11, 1.0)
        self.assertRaises(TypeError, Hero, 11, 5, 706)

    def test_from_name(self):
        # create hero from valid name
        Hero.from_name('Underlord')

        # creation from the in_game_name should be valid too
        Hero.from_name('antimage')

        # test creation of the Hero from misspelled name
        self.assertRaises(ValueError, Hero.from_name, 'Antimage')

        # call with non-string, just in case
        self.assertRaises(TypeError, Hero.from_name, 4)

    def test_get_description(self):
        # call with empty include argument
        self.assertRaises(TypeError, self.sf_1.get_description)
        # test if `include` does not contain any of possible fields
        self.assertRaises(ValueError, self.sf_1.get_description, ['asd'])
        # empty include list
        self.assertRaises(ValueError, self.sf_1.get_description, [])
        # test if one of the `include`d is possible and one is not
        self.assertEqual((1,),
                         self.sf_1.get_description(['name', 'asd']).shape)

    def test_patches(self):
        ''' Tests that hero reads only data from needed patch.

        If there are some patches in table, Hero should contain only one set
        of abilities assigned with the right patch.
        '''

        self.assertEqual(len(self.sf_1.abilities), 6)

    def test_primary_attribute(self):
        self.assertEqual(self.sf_1.primary_attribute, 'agility')
        self.assertEqual(Hero(1).primary_attribute, 'agility')
        self.assertEqual(Hero(2).primary_attribute, 'strength')

    def test_camel2python(self):
        test_data = {'PrimaryAttribute': 'primary_attribute',}

        for test_str, output in test_data.items():
            self.assertEqual(camel2python(test_str), output)


if __name__ == '__main__':
    unittest.main()
