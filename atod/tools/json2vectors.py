#!/usr/bin/env python3
''' Set of functions to transform dict (json) to pandas.DataFrame. '''

import os
import re
import json
import pandas
from sklearn.preprocessing import LabelEncoder, OneHotEncoder

from atod import settings


def get_keys(dict_):
    ''' Finds list of all the keys in given dict recursively.

        Except for fixme keys.
    '''
    all_keys = set()
    for key in dict_:
        if isinstance(dict_[key], dict):
            all_keys = all_keys.union(get_keys(dict_[key]))

        # FIXME: move this from function
        # I don't need this keys for now
        elif key != 'var_type' and key != 'Version':
            all_keys.add(key)

    return all_keys


def make_flat_dict_(dict_):
    ''' Moves all the properties of inserted dicts to the top level.

        Example {'a': 1, 'b':{'c':3, 'd':4}} -> {'a':1, 'c':3, 'b':4}
    '''
    result = []
    # the reason for this is described in TestJson2Vectors fixme
    if isinstance(dict_, str):
        return []

    for k, v in dict_.items():
        if isinstance(v, str):
            # I don't need this key for now
            if k == 'var_type' or k == 'Version':
                continue
            result.append({k: v})
        else:
            result.extend(make_flat_dict_(v))

    return result


def make_flat_dict(dict_):
    ''' Wrapper for recursive make_flat_dict_().

        :Args:
            dict_ (dict) : to make flat

        :Returns:
            flat (dict) : described in make_flat_dict_()
    '''
    # get array of one-element dicts
    dicts = make_flat_dict_(dict_)
    result = {}
    for d in dicts:
        key = list(d.keys())[0]
        result[key] = d[key]

    return result


def to_vectors(filename, write_to_file=False):
    ''' Function to call from outside of the module.

        :Args:
            filename (str) : file from which func will extract vectors

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

    columns = get_keys(data)

    S = {}
    for key, value in data.items():
        if any(map(lambda hero: hero in key, heroes_names)):
            flat = make_flat_dict(value)
            vector = [flat[e] if flat.get(e, None) else 0 for e in effects]
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

    effects = get_keys(data)

    S = {}
    for key, value in data.items():
        # get only playable heroes skills
        if any(map(lambda hero: hero in key, heroes_names)):
            flat = make_flat_dict(value)
            vector = [1 if flat.get(e, None) else 0 for e in effects]
            S[key] = pandas.Series(vector, effects)

    return pandas.DataFrame(S)


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

    damage_effects  = [e for e in effects_list if 'damage' in e]
    move_effects    = [e for e in effects_list if 'move' in e]
    healing_effects = [e for e in effects_list if
                               any(map(lambda x: x in e, heal_words))]
    durations       = [e for e in effects_list if 'duration' in e]
    # TODO: same for illusions, replicas
    # TODO: same for reductions, probably

    print(len(damage_effects))
    print(len(move_effects))
    print(len(healing_effects))
    print(len(durations))

    D = abilities[damage_effects]
    D = D.dropna(0, thresh=1)
    D = D.dropna(1, thresh=1)

    D.T.to_excel(settings.DATA_FOLDER + 'damage_effects.xlsx')

    print(D)


def get_all_values(input_dict):
    ''' Finds all possible values of categorical variables.

        :Args:
            keys (list of strings) : variables to find values

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


if __name__ == '__main__':
    with open(settings.ABILITIES_FILE, 'r') as fp:
        abilities = json.load(fp)
    values = get_all_values(abilities)

    encoding = create_encoding(values)
    vectors = to_vectors(settings.ABILITIES_FILE)
    print(vectors)
