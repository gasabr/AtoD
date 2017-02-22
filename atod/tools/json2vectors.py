#!/usr/bin/env python3
''' Set of functions to transform dict (json) to pandas.DataFrame. '''

import json
import pandas

from atod import settings


def get_keys(dict_):
    ''' Finds list of all the keys in given dict recursively. '''
    all_keys = set()
    for key in dict_:
        if isinstance(dict_[key], dict):
            all_keys = all_keys.union(get_keys(dict_[key]))

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


def to_vectors(filename):
    ''' Function to call from outside of the module.

        :Args:
            filename (str) : file from which func will extract vectors

        :Returns:
            table (pandas.DataFrame) : DataFrame of extracted vectors
    '''
    # load converter to filter keys
    with open(settings.IN_GAME_CONVERTER, 'r') as fp:
        converter = json.load(fp)

    # TODO: try-catch here
    with open(filename, 'r') as fp:
        data = json.load(fp)

    # if there is global key, get rid of it
    if len(data) == 1:
        global_key = list(data.keys())[0]
        data = data[global_key]

    print(len(data))

    columns = get_keys(data)

    S = {}
    for key, value in data.items():
        if any(map(lambda hero: hero in key, converter.keys())):
            flat = make_flat_dict(value)
            S[key] = pandas.Series([flat.get(k, None) for k in columns], columns)

    result_frame = pandas.DataFrame(S)

    return result_frame


if __name__ == '__main__':
    filename = settings.ABILITIES_FILE
    to_vectors(filename)
