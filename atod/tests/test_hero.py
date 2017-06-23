#!/usr/bin/env python3
import unittest

from atod.models.heroes import Hero, camel2python


class TestHero(unittest.TestCase):

    def setUp(self):
        ''' Creates 2 Shadow Fiends to test methods. '''
        self.sf_1 = Hero(11)
        self.sf_10 = Hero(11, 10)

    def test_init(self):
        ''' Tests different ways to create hero. '''
        self.assertRaises(TypeError, Hero, 'Earthshaker')
        self.assertRaises(TypeError, Hero, 11, 1.0)
        self.assertRaises(TypeError, Hero, 11, 5, 706)

        # test creation of the Hero from name
        # misspeled name
        self.assertRaises(ValueError, Hero.from_name, 'Antimage')

    def test_get_description(self):
        # call with empty include argument
        self.assertRaises(TypeError, self.sf_1.get_description)
        # test if `include` does not contain any of possible fields
        self.assertRaises(ValueError, self.sf_1.get_description, ['asd'])
        # test if one of the `include`d is possible and one is not
        self.assertEqual((1,),
                         self.sf_1.get_description(['name', 'asd']).shape)

    def test_patches(self):
        ''' Tests that hero reads only data from needed patch. 
        
        If there are some patches in table, Hero should contain only one set
        of abilities assigned with the right patch.
        '''

        self.assertEqual(len(self.sf_1.abilities), 6)

    def test_camel2python(self):
        test_data = {'PrimaryAttribute': 'primary_attribute',}

        for test_str, output in test_data.items():
            self.assertEqual(camel2python(test_str), output)


if __name__ == '__main__':
    unittest.main()
