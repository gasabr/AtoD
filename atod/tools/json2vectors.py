#!/usr/bin/env python3
''' Set of functions to transform dict (json) to pandas.DataFrame. '''

import os
import re
import json
import pandas
from sklearn.preprocessing import LabelEncoder

from atod import settings

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


def find_words_in_keys(abilities):
    ''' Finds all the words in keys of given dictionary. '''
    # all the keys in the dictionary
    keys = get_keys(abilities, exclude=['Version', 'var_type'])

    # all the possible 'elementary' effects in abilities
    words = set()
    for k in keys:
        if len(k.split('_')) > 1:
            words = words.union(k.split('_'))
        # FIXME: check categorical keys here if needed
        elif k != 'ID':
            words.add(k)

    return words


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


def get_keys(dict_, exclude=[]):
    ''' Finds list of all the keys in given dict recursively. '''
    all_keys = set()
    for key in dict_:
        if isinstance(dict_[key], dict):
            all_keys = all_keys.union(get_keys(dict_[key], exclude=exclude))

        elif key not in exclude:
            all_keys.add(key)

    return all_keys


def collect_kv(dict_, exclude=[]):
    ''' Finds all pairs key-value in all dictionaries inside given.

        Example {'a': 1, 'b':{'c':3, 'd':4}} -> [{'a':1}, {'c':3}, {'b':4}]
        On the next step make_flat_dict will transform result of this
        function to the flat dict.
    '''
    kv_pairs = []
    # the reason for this is described in TestJson2Vectors fixme
    if not isinstance(dict_, dict):
        return []

    for k, v in dict_.items():
        if isinstance(v, str) or isinstance(v, int) or isinstance(v, float):
            if k in exclude:
                continue
            kv_pairs.append({k: v})
        elif isinstance(v, list):
            kv_pairs.append({k: sum(v)/len(v)})
        else:
            kv_pairs.extend(collect_kv(v, exclude=exclude))

    return kv_pairs


def make_flat_dict(dict_, exclude=[]):
    ''' Wrapper for recursive collect_kv().

        :Args:
            dict_ (dict) : to make flat

        :Returns:
            flat (dict) : described in collect_kv()
    '''
    # get array of one-element dicts
    exclude.extend(['Version', 'var_type'])
    dicts = collect_kv(dict_, exclude=exclude)
    result = {}
    for d in dicts:
        key = list(d.keys())[0]
        result[key] = d[key]

    return result


def get_all_values(input_dict):
    ''' Finds all possible values of categorical variables.

            :Args:
                input_dict (dict) : dict to search

            :Returns:
                values (dict) : {key: [value1, value2,...], }
        '''

    values = {}
    for key, value in input_dict.items():
        # if value is string add it to possible values
        if key not in values.keys():
            values[key] = []

        if isinstance(value, str) and len(re.findall(r'[a-zA-Z]+', value)) > 0:
            # values can be separated by ' | ' to handle this:
            split_value = value.split('|')
            # to handle one syntax error in file
            split_value = [s.replace(' ', '') for s in split_value if
                           s != ' ']

            values[key].extend(split_value)

        # if value is a dict add it to DFS stack
        if isinstance(value, dict):
            # r<name> stands for recursively gotten
            rvalues = get_all_values(value)
            for rkey, rvalue in rvalues.items():
                if rkey in values.keys():
                    values[rkey].extend(rvalue)
                else:
                    values[rkey] = rvalue

    return values


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

    all_values = get_all_values(abilities)
    encoding = create_encoding(all_values)
    # cat stands for categorical
    cat_columns = ['{}={}'.format(k, vv) for k, v in encoding.items()
                           for vv in v if k != 'var_type' and
                                          k != 'LinkedSpecialBonus' and
                                          k != 'HotKeyOverride' and
                                          k != 'levelkey'
                                          ]

    heroes_abilities = find_heroes_abilities(abilities, exclude=encoding.keys())
    effects = find_words_in_keys(abilities)

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

    all_values = get_all_values(abilities)
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
    set_of_features = get_keys(abilities, exclude)
    print(sorted(set_of_features))
