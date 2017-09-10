import unittest
import pandas as pd

from atod import Ability


class TestAbility(unittest.TestCase):
    def test_init(self):
        # create ability with non existent id
        self.assertRaises(ValueError, Ability, 14)
        self.assertRaises(TypeError, Ability, 11, 1.0)
        self.assertRaises(TypeError, Ability, 11, 5, 706)

    def test_description_output_type(self):
        ''' Tests type validness on good output. '''
        t = Ability(5012)
        self.assertIsInstance(
                t.get_description(['texts', 'name']), 
                pd.Series
                )

    def test_get_texts_output_type(self):
        t = Ability(5024)
        self.assertIsInstance(
                t.get_texts(),
                pd.Series
                )

    def test_get_specs_output_type(self):
        t = Ability(5024)
        self.assertIsInstance(
                t.get_specs(),
                pd.Series
                )


if __name__ == '__main__':
    unittest.main()
