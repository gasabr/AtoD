#!/usr/bin/env python3
''' Set of functions to transform dict (json) to pandas.DataFrame. '''

import os
import re
import json
import pandas
from sklearn.preprocessing import LabelEncoder

from atod import settings
from atod.tools.dictionary import (make_flat_dict, extract_effects, all_keys,
                                   find_all_values)

#===============================================================================
# List of functions on npc_abilities.json
#===============================================================================

# IDEA: modify function to work with talents too
def find_heroes_abilities(abilities, exclude=[]):
    ''' Talents are not included. '''
    # load converter to get heroes names
    with open(settings.IN_GAME_CONVERTER, 'r') as fp:
        converter = json.load(fp)

    heroes_names = [c for c in converter.keys()
                    if re.findall(r'[a-zA-Z|\_]+', c)]

    # find all the heroes skills, but not talents
    heroes_abilities = set()
    for key, value in abilities.items():
        # if ability contains hero name, doesn't contain special_bonus
        if any(map(lambda name: name in key, heroes_names)) and \
                    'special_bonus' not in key and \
                    'empty' not in key and \
                    'scepter' not in key and \
                    key not in exclude:
            heroes_abilities.add(key)

    return heroes_abilities


def create_numeric(data, rows, columns):
    ''' Creates part from numeric variables in binary vectors DataFrame. '''
    # DataFrame(abilities X effects)
    numeric = pandas.DataFrame([], index=rows, columns=columns)
    # TODO: logger.info('DataFrame with abilities created',
    #       'shape={}'.format(frame.shape))

    # fill DataFrame
    for key, values in numeric.iterrows():
        for e in list(values.index):
            # if this effect is inside any key of the ability
            values[e] = 1 if any(map(lambda k: e in k, data[key].keys())) else 0

    return numeric


def create_categorical(data, rows, columns):
    ''' Creates part from categorical variables in binary vectors DataFrame. '''
    # categoriacal features in ability descrition
    categorical = pandas.DataFrame([], index=rows, columns=columns)

    # fill categorical_part
    for skill, values in categorical.iterrows():
        categorical.loc[skill] = categorical.loc[skill].fillna(value=0)
        # for all the categorical variables
        for cat_var in columns:
            try:
                # check if this ability has such categorical variable
                getattr(data[skill], cat_var)
            except AttributeError as e:
                continue

            cat_values = data[skill][cat_var].split(' | ')

            if len(cat_values) == 1:
                column_to_write = '{}={}'.format(cat_var, cat_values[0])
                categorical.loc[skill][column_to_write] = 1
            else:
                for c in cat_values:
                    categorical.loc[skill]['{}={}'.format(cat_var, c)] = 1

#===============================================================================

def lists_to_mean(dict_):
    ''' Changes all the lists to their mean. '''
    for key in dict_.keys():
        if isinstance(dict_[key], list):
            dict_[key] = sum(dict_[key])/len(dict_[key])
        if isinstance(dict_[key], dict):
            lists_to_mean(dict_[key])

    return


def create_encoding(values):
    ''' Maps categorical values to numbers with LabelEncoder.

        :Args:
            values (dict) : {"variable_name": "possible_value"}

        :Returns:
            encoding (dict) : {"variable_name": {"possible_value": encoding,},}
    '''

    encoding = {}
    number = LabelEncoder()

    for var_name, values in values.items():
        encoded = number.fit_transform(values).astype('str')

        for value, e in zip(values, encoded):
            if not encoding.get(var_name, None):
                encoding[var_name] = {}

            encoding[var_name][value] = e

    return encoding


def to_bin_vectors(filename):
    ''' Function to call from outside of the module.

        :Args:
            filename (str) : file from which func will extract vectors

        :Returns:
            table (pandas.DataFrame) : DataFrame of extracted vectors
    '''

    # load parsed npc_abilities.txt file
    with open(filename, 'r') as fp:
        abilities = json.load(fp)['DOTAAbilities']

    for ability, features in abilities.items():
        if isinstance(features, dict):
            features = make_flat_dict(features)

    all_values = find_all_values(abilities)
    encoding = create_encoding(all_values)
    # cat stands for categorical
    cat_columns = ['{}={}'.format(k, vv) for k, v in encoding.items()
                           for vv in v if k != 'var_type' and
                                          k != 'LinkedSpecialBonus' and
                                          k != 'HotKeyOverride' and
                                          k != 'levelkey'
                                          ]

    heroes_abilities = find_heroes_abilities(abilities, exclude=encoding.keys())
    effects = extract_effects(heroes_abilities)

    numeric_part = create_numeric(abilities, heroes_abilities, effects)
    categoriacal_part = create_categorical(abilities,
                                           heroes_abilities,
                                           encoding.keys()
                                           )
    result_frame = pandas.concat([numeric_part, categoriacal_part], axis=1)

    return result_frame


def to_vectors(filename):
    ''' Creates '''
    # load parsed npc_abilities.txt file
    with open(filename, 'r') as fp:
        abilities = json.load(fp)['DOTAAbilities']

    all_values = find_all_values(abilities)
    encoding = create_encoding(all_values)
    # cat stands for categorical
    cat_columns = ['{}={}'.format(k, vv) for k, v in encoding.items()
                           for vv in v if k != 'var_type' and
                                          k != 'LinkedSpecialBonus' and
                                          k != 'HotKeyOverride' and
                                          k != 'levelkey'
                                          ]

    heroes_abilities = find_heroes_abilities(abilities, exclude=encoding.keys())
    exclude = list(encoding.keys()) + ['Version', 'var_type']
    set_of_features = list(all_keys(abilities, exclude))
    print(sorted(set_of_features))
