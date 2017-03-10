#!/usr/bin/env python3
'''Set of functions on dict needed for different parts of the program.'''
import re
from sklearn.preprocessing import LabelEncoder


def all_keys(dict_, exclude=[], include_dict_keys=True):
    '''Finds list of all the keys in given dict recursively.'''
    for key in dict_:
        if key not in exclude:
            if isinstance(dict_[key], dict):
                for k in all_keys(dict_[key], exclude, include_dict_keys):
                    yield k
                if include_dict_keys:
                    yield key
            else:
                yield key


def extract_effects(effects):
    '''Finds all the words in keys of given dictionary.'''
    return (e for effect in effects for e in effect.split('_'))


def collect_kv(dict_, exclude=[]):
    ''' Finds all pairs key-value in all dictionaries inside given.

        On the next step make_flat_dict will transform result of this
        function to the flat dict.

        Args:
            dict_ (dict): to search for pairs
            exclude (list): except for this keys

        Returns:
            kv_pairs (list): see examples

        Examples:
            >>> di = {'a': 1, 'b':{'c':3, 'd':4}}
            >>> collect_kv(di)
            [{'a':1}, {'c':3}, {'d':4}]
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
    ''' Turns dictionary with nested dictionaries into a flat one.

        Flat means that all nested key-value pairs are stored on the top level.

        Args:
            dict_ (dict) : to make flat
            exclude (list): this keys would be skipped over

        Returns:
            flat (dict) : described in collect_kv()

        Examples:
            >>> d = {'a':1, b:{'c':2}}
            >>> make_flat_dict(d)
            {'a':1, 'c':2}
    '''
    # get array of one-element dicts
    exclude.extend(['Version', 'var_type'])
    dicts = collect_kv(dict_, exclude=exclude)
    result = {}
    for d in dicts:
        key = list(d.keys())[0]
        result[key] = d[key]

    return result


def find_all_values(input_dict):
    ''' Finds all possible values of categorical variables.

        Args:
            input_dict (dict) : dict to search

        Returns:
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
            split_value = [s.replace(' ', '') for s in split_value if s != ' ']

            values[key].extend(split_value)

        # if value is a dict call function recursively
        if isinstance(value, dict):
            # r<name> stands for recursively gotten
            rvalues = find_all_values(value)
            for rkey, rvalue in rvalues.items():
                if rkey in values.keys():
                    values[rkey].extend(rvalue)
                else:
                    values[rkey] = rvalue

    return {k: list(set(v)) for k, v in values.items() if len(v) > 0}


def create_encoding(values):
    ''' Maps categorical values to numbers with LabelEncoder.

        Args:
            values (dict) : result of find_all_values()

        Returns:
            encoding (dict) : {"var_name": ["value1", "value2"]}
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
