#!/usr/bin/env python3
''' Set of functions to transform dict (json) to pandas.DataFrame. '''

import json
import pandas

from atod import settings

filename = settings.DATA_FOLDER + 'from-game/items.json'
items = {}
with open(filename, 'r') as fp:
    items_data = json.load(fp)

basic_features = set()
items_list = set()


def get_keys(dict_):
    ''' Finds list of all the keys in given dict recursively. '''
    all_keys = set()
    for key in dict_:
        if isinstance(dict_[key], dict):
            all_keys = all_keys.union(get_keys(dict_[key]))
        else:
            all_keys.add(key)

    return all_keys


def make_flat_dict_(dict_):
    ''' Moves all the properties of inserted dicts to the top level.

        Example {'a': 1, 'b':{'c':3, 'd':4}} -> {'a':1, 'c':3, 'b':4}
    '''
    result = []
    for k, v in dict_.items():
        if isinstance(v, str):
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
    # TODO: try-catch here
    with open(filename, 'r') as fp:
        data = json.load(fp)

    # if there is global key, get rid of it
    if len(data) == 1:
        global_key = list(data.keys())[0]
        data = data[global_key]

    keys = get_keys(data)

    example = data[list(data.keys())[0]]
    print(json.dumps(example, indent=2))
    example_flat = make_flat_dict(example)
    print()
    print(json.dumps(example_flat, indent=2))


if __name__ == '__main__':
    filename = settings.ABILITIES_FILE
    to_vectors(filename)
