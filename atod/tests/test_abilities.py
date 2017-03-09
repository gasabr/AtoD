import os
import json
import unittest

from atod import settings
from atod.abilities import abilities as Abilities
from atod.tools.dictionary import make_flat_dict
from atod.tools.abilities import create_numeric, create_categorical


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

    def test_frame_shape(self):
        expected_shape = (len(Abilities.skills),
                          len(Abilities.cat_columns) + len(self.effects))

        self.assertEqual(expected_shape, self.frame.shape)


class TestToolsAbilities(unittest.TestCase):

    def setUp(self):
        self.data_folder = os.path.join(settings.TESTS_DATA_FOLDER
                                        + 'abilities/')

    def test_numeric(self):
        with open(self.data_folder + 'savage_roar.json') as fp:
            data = json.load(fp)

        # dataset from one ability
        for key, value in data.items():
            data[key] = make_flat_dict(value)
            result = create_numeric(data,
                                    [list(data)],
                                    [e for key in data[key]
                                       for e in key.split('_')])

            self.assertEqual(sum(result.ix[0]), len(result.ix[0]))

        # one ability, but custom columns
        for key, value in data.items():
            data[key] = make_flat_dict(value)
            result = create_numeric(data,
                                    [list(data)],
                                    ['duration', 'bonus', 'speed', 'slow',
                                     'stun', 'silence'])

            self.assertEqual(sum(result.ix[0]), 3)
            self.assertEqual(result.ix[0]['duration'], 1)
            self.assertEqual(result.ix[0]['bonus'], 1)
            self.assertEqual(result.ix[0]['slow'], 0)
            self.assertEqual(result.ix[0]['silence'], 0)


    def test_categorical(self):
        with open(self.data_folder + 'savage_roar.json') as fp:
            data = json.load(fp)

        cat_columns = Abilities.cat_columns

        for key, value in data.items():
            data[key] = make_flat_dict(value)
            result = create_categorical(data, [list(data)], cat_columns)

            self.assertEqual(1, result.loc[key]['AbilityBehavior=DOTA_ABILITY_BEHAVIOR_NO_TARGET'])
            self.assertEqual(1, result.loc[key]['AbilityBehavior=DOTA_ABILITY_BEHAVIOR_HIDDEN'])
            self.assertEqual(1, result.loc[key]["SpellDispellableType=SPELL_DISPELLABLE_YES"])



if __name__ == '__main__':
    unittest.main()
