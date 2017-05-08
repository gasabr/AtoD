#!/usr/bin/env python3
'''Set of functions on dict needed for different parts of the program.'''
import re
import logging
from sklearn.preprocessing import LabelEncoder


def all_keys(dict_, exclude=[], include_dict_keys=True):
    ''' Finds list of all the keys in given dict recursively.
     
        Notes:
            To get all different keys use: set(all_keys(your_dict))
    
        Yields:
            key: single key from the dictionary.
    '''
    for key in dict_:
        if key not in exclude:
            if isinstance(dict_[key], dict):
                for k in all_keys(dict_[key], exclude, include_dict_keys):
                    yield k
                if include_dict_keys:
                    yield key
            else:
                yield key


def count_keys(dictionary):
    ''' Counts times when keys occur in a dictionary.

        Args:
            dictionary (dict): dictionary to count

        Returns:
            key2occur (dict): key mapped to occurrences
    '''

    key2occur = dict()
    for key, value in dictionary.items():
        key2occur.setdefault(key, 0)
        key2occur[key] += 1

        if isinstance(value, dict):
            rec = count_keys(value)
            for k, v in rec.items():
                key2occur.setdefault(k, 0)
                key2occur[k] += v

    return key2occur


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
            kv_pairs (list): 
    '''
    kv_pairs = []
    if not isinstance(dict_, dict):
        return []

    for k, v in dict_.items():
        if isinstance(v, dict):
            kv_pairs.extend(collect_kv(v, exclude=exclude))
        elif k not in exclude:
            kv_pairs.append({k: v})

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
            >>> d = {'a':1, 'b':{'c':2}}
            >>> make_flat_dict(d)
            {'a':1, 'c':2}
    '''
    # get array of one-element dicts
    # TODO: remove this strange thing
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


def find_keys(dict_, keywords=[], mode='any'):
    ''' Returns all the hero abilities.

        Args:
            dict_ (dict): dictionary to search keywords in
            keywords (list): words to be found in skills
            mode (str): 'all' or 'any' defines which keywords
                should be found in key for him to added to result

        Returns:
            abilities_ (list): list of Ability
    '''

    if len(keywords) == 0:
        logging.warning('No keys in find_properties() call.')
        return []

    properties = dict()
    for key, value in dict_.items():
        if mode == 'any':
            props = find_keys_any(value, keywords)
            if len(props) == 0:
                continue
            properties[key] = {p[0]: p[1] for p in props}

    return properties


def find_keys_any(dict_, keywords=[]):
    ''' Searches for properties which contain any of keywords.

        Args:
            dict_ (dict): dict to search into
            keywords (iterable of strings): words which should be found

        Returns:
            properties (list of tuples): tuple example ('property', 1)
    '''
    properties = list()
    for property_, value in dict_.items():
        for k in keywords:
            if k in property_:
                properties.append((property_, value))

    return properties


def get_types(dict_):
    ''' Defines types of values in dictionary.
    
        If the value is a list, set or tuple, all the types would be 
        added. Dictionary would be added as dict, not types of values.
    
        Args:
            dict_ (dict): dictionary to define types
            
        Returns:
            types (dict): keys to list of values types
    '''

    types = dict()
    for key, value in dict_.items():
        types.setdefault(key, set())

        if isinstance(value, (list, set, tuple)):
            types[key] = types[key].union([type(i) for i in value])
        else:
            types[key].add(type(value))

    return types


def get_str_keys(dict_):
    ''' Returns:
            keys which contain only alphabet chars
    '''
    return [c for c in dict_.keys() if re.findall(r'[a-zA-Z|\_]+', c)]