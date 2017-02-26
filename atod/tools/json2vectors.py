#!/usr/bin/env python3
''' Set of functions to transform dict (json) to pandas.DataFrame. '''

import os
import re
import json
import pandas
from sklearn.preprocessing import LabelEncoder, OneHotEncoder

from atod import settings


def lists_to_mean(dict_):
    ''' Changes all the lists to their mean. '''
    for key in dict_.keys():
        if isinstance(dict_[key], list):
            dict_[key] = sum(dict_[key])/len(dict_[key])
        if isinstance(dict_[key], dict):
            lists_to_mean(dict_[key])

    return


def get_keys(dict_, except_=[]):
    ''' Finds list of all the keys in given dict recursively.

        Except for fixme keys.
    '''
    all_keys = set()
    for key in dict_:
        if isinstance(dict_[key], dict):
            all_keys = all_keys.union(get_keys(dict_[key]))

        # FIXME: move this from function
        # I don't need this keys for now
        elif key not in except_:
            all_keys.add(key)

    return all_keys


def collect_kv(dict_, except_=[]):
    ''' Finds all pairs key-value in all dictionaries incside given.

        Example {'a': 1, 'b':{'c':3, 'd':4}} -> [{'a':1}, {'c':3}, {'b':4}]
        On the next step make_flat_dict will transform result of this
        function to the flat dict.
    '''
    kv_pairs = []
    # the reason for this is described in TestJson2Vectors fixme
    if not isinstance(dict_, dict):
        return []

    for k, v in dict_.items():
        if isinstance(v, str):
            if k in except_:
                continue
            kv_pairs.append({k: v})
        else:
            kv_pairs.extend(collect_kv(v))

    return kv_pairs


def make_flat_dict(dict_):
    ''' Wrapper for recursive collect_kv().

        :Args:
            dict_ (dict) : to make flat

        :Returns:
            flat (dict) : described in collect_kv()
    '''
    # get array of one-element dicts
    dicts = collect_kv(dict_, except_=['Version', 'var_type'])
    result = {}
    for d in dicts:
        key = list(d.keys())[0]
        result[key] = d[key]

    return result


def to_vectors(filename, write_to_file=False):
    ''' Transform dictionaries data to vectors of features.

        :Args:
            filename (str) : file from which func will extract vectors
            write_to_file (bool) : output_filename=abilities_vectors.json

        :Returns:
            table (pandas.DataFrame) : DataFrame of extracted vectors
    '''
    # load converter to filter keys
    with open(settings.IN_GAME_CONVERTER, 'r') as fp:
        converter = json.load(fp)

    heroes_names = [c for c in converter.keys()
                            if re.findall(r'[a-zA-Z|\_]+', c)]

    # TODO: try-catch here
    with open(filename, 'r') as fp:
        data = json.load(fp)

    # if there is global key, get rid of it
    if len(data) == 1:
        global_key = list(data.keys())[0]
        data = data[global_key]

    columns = get_keys(data, except_=['Version', 'var_type'])

    S = {}
    for key, value in data.items():
        if any(map(lambda hero: hero in key, heroes_names)):
            flat = make_flat_dict(value)
            vector = [flat[e] if flat.get(e, None) else 0 for e in columns]
            S[key] = pandas.Series(vector, columns)

    result_frame = pandas.DataFrame(S)

    if write_to_file:
        filename = os.path.join(settings.DATA_FOLDER, 'abilities_vectors.json')
        result_frame.to_json(filename, orient='index')

    return result_frame


def to_bin_vectors(filename):
    ''' Function to call from outside of the module.

        :Args:
            filename (str) : file from which func will extract vectors

        :Returns:
            table (pandas.DataFrame) : DataFrame of extracted vectors
    '''
    # load converter to get heroes names
    with open(settings.IN_GAME_CONVERTER, 'r') as fp:
        converter = json.load(fp)

    heroes_names = [c for c in converter.keys()
                            if re.findall(r'[a-zA-Z|\_]+', c)]

    # load parsed npc_abilities.txt file
    with open(filename, 'r') as fp:
        abilities = json.load(fp)['DOTAAbilities']

    # all the keys in the dictionary
    keys = get_keys(abilities, except_=['Version', 'var_type'])

    # cat stands for categorical
    all_values = get_all_values(abilities)
    encoding = create_encoding(all_values)
    cat_columns = ['{}={}'.format(k, vv) for k, v in encoding.items()
                           for vv in v if k != 'var_type' and
                                          k != 'LinkedSpecialBonus' and
                                          k != 'HotKeyOverride'
                  ]
    # FIXME: remove this keys: 'var_type', 'LinkedSpecialBonusOperation', 'levelkey',
    #    'AbilitySharedCooldown', 'AbilityUnitTargetFlag',
    #    'AbilityUnitTargetType', 'AbilityUnitDamageType',
    #    'SpellDispellableType', 'AbilityUnitTargetTeam', 'SpellImmunityType'

    # all the possible 'elementary' effects in abilities
    effects = set()
    for k in keys:
        if len(k.split('_')) > 1:
            effects = effects.union(k.split('_'))
        else:
            effects.add(k)

    # find all the heroes skills, but not talents
    heroes_abilities = set()
    for key, value in abilities.items():
        if any(map(lambda name: name in key, heroes_names)) and \
                    'special_bonus' not in key and \
                    key not in encoding.keys():
            heroes_abilities.add(key)

    # DataFrame(abilities X effects)
    frame = pandas.DataFrame([], index=heroes_abilities, columns=effects)
    print(frame.shape)

    for key, values in frame.iterrows():
        for e in list(values.index):
            # if this effect is inside any key of the ability
            values[e] = 1 if any(map(lambda k:
                                     e in k, abilities[key].keys())) else 0

    cat_part = pandas.DataFrame([], index=heroes_abilities, columns=cat_columns)

    # fill categorical_part
    # for all rows in the DataFrame
    for skill, values in cat_part.iterrows():
        # for all the categorical variables
        for cat_var in encoding.keys():
            try:
                # check if this ability has such categorical variable
                abilities[skill][cat_var]
            except KeyError as e:
                cat_part.loc[cat_var] = -1
                continue

            cat_values = abilities[skill][cat_var].split(' | ')

            if len(cat_values) == 1:
                cat_part.loc[skill]['{}={}'.format(cat_var, cat_values[0])] = 1
            else:
                for c in cat_values:
                    cat_part.loc[skill]['{}={}'.format(cat_var, c)] = 1

    cat_part = cat_part.fillna(0)
    print(cat_part.index)


def get_similar_effects():
    ''' Finds similar features.

        There are a lot of skills with similar effects: stuns, heals...
        but their effects stored in different variables inside attributes file.
        This function is aimed to collect effects by similarity in the name.
    '''
    abilities = to_vectors(settings.ABILITIES_FILE).T

    print(abilities.index)

    # drop all the scepter effects
    effects_list = [e for e in list(abilities.columns) if 'scepter' not in e]

    heal_words = ['heal', 'restore', 'hp', 'regen']

    damage_effects  = [e for e in effects_list if 'damage' in e and
                       'illusion' not in e and 'replica' not in e]
    move_effects    = [e for e in effects_list if 'move' in e]
    healing_effects = [e for e in effects_list if
                               any(map(lambda x: x in e, heal_words))]
    durations       = [e for e in effects_list if 'duration' in e]
    stuns           = [e for e in effects_list if 'stun' in e]
    # TODO: same for illusions, replicas
    # TODO: same for reductions, probably

    print(len(damage_effects))
    # print(damage_effects)
    print(len(move_effects))
    print(len(healing_effects))
    print(len(durations))
    print(len(stuns))

    D = abilities[damage_effects]
    D = D.dropna(1)
    D = D.dropna(0)

    print(D.shape)

    # D.T.to_excel(settings.DATA_FOLDER + 'damage_effects.xlsx')

    # print(D)


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
            splitted_value = value.split('|')
            # to handle one syntax error in file
            splitted_value = [s.replace(' ', '') for s in splitted_value if
                              s != ' ']

            values[key].extend(splitted_value)

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

    values_list = []
    encoding = {}
    number = LabelEncoder()

    for var_name, values in values.items():
        encoded = number.fit_transform(values).astype('str')

        for value, e in zip(values, encoded):
            if not encoding.get(var_name, None):
                encoding[var_name] = {}

            encoding[var_name][value] = e

    return encoding


def to_frame(filename):
    ''' Turns file into the pandas.DataFrame.

        All the lists are replaced with their means.
        All the categorical variables replaced with OneHotEncoding.
    '''
    with open(filename, 'r') as fp:
        data = json.load(fp)

    flat_data = make_flat_dict(data)
    # lists changes given data
    lists_to_mean(data)
    values = get_all_values(data)
    encoding = create_encoding(values)

    print(json.dumps(encoding, indent=2))

    keys = get_keys(data, except_=['Version', 'var_type'])

    effects = set()
    for k in keys:
        if len(k.split('_')) > 1:
            effects = effects.union(k.split('_'))
        else:
            effects.add(k)

    print(sorted(effects))


if __name__ == '__main__':
    to_bin_vectors(settings.ABILITIES_FILE)
    # get_similar_effects()
    # to_frame(settings.ABILITIES_FILE)
