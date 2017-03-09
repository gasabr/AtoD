import unittest

from atod.abilities import abilities as Abilities


class TestAbilities(unittest.TestCase):

    def setUp(self):
        self.frame   = Abilities.frame
        self.effects = Abilities.effects

    def test_effects_extraction(self):
        '''Tests effect property.'''
        # check if every key split to words
        for e in self.effects:
            self.assertEqual(False, '_' in e)

        # check if every word in skills occurs in effects
        for skill, description in Abilities.skills.items():
            for key in description:
                for effect in key.split('_'):
                    self.assertEqual(True, effect in self.effects)


if __name__ == '__main__':
    unittest.main()
