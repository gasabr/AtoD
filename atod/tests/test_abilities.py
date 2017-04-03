import json
import os
import unittest

from atod import settings
from atod.abilities import abilities as Abilities
from atod.modeling.abilities import (encode_effects,
                                     create_categorical)
from atod.preprocessing.clean_abilities import clean \
    as get_clean_abilities
from atod.preprocessing.dictionary import make_flat_dict


class TestAbilities(unittest.TestCase):

    def test_effects_extraction(self):
        '''Tests effects property.'''
        # check if every key split to words
        effects = Abilities.effects
        for e in effects:
            self.assertEqual(False, '_' in e)

        # check if every word in skills occurs in effects
        for skill, description in Abilities.skills.items():
            for key in description:
                for effect in key.split('_'):
                    self.assertEqual(True, effect in effects)

    def test_frame_shape(self):
        ''' Very long test, since whole DataFrame is created.'''
        clean_abilities = get_clean_abilities()
        properties = Abilities.get_properties()
        frame = Abilities.clean_frame
        expected_shape = (len(clean_abilities),
                          len(Abilities.cat_columns) + len(properties))

        self.assertEqual(expected_shape, frame.shape)


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
            result = encode_effects(data,
                                    [list(data)],
                                    [e for key in data[key]
                                       for e in key.split('_')])

            self.assertEqual(sum(result.ix[0]), len(result.ix[0]))

        # one ability, but custom columns
        for key, value in data.items():
            data[key] = make_flat_dict(value)
            result = encode_effects(data,
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
