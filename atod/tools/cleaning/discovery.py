''' Set of functions which help to understand data and see what can be
    cleaned.
'''

import json
import logging

from atod.tools import dictionary
from atod.tools.cleaning import abilities

def print_keys_occurrences():
    data = abilities.main()
    key2occur = dictionary.count_keys(data)

    # remove abilities names from key2occur
    for ability_name in data:
        if ability_name in key2occur.keys():
            del key2occur[ability_name]

    keys_by_occur = sorted(key2occur, key=key2occur.get)
    for key in keys_by_occur:
        print(key, '->', key2occur[key])


def find_properties(dict_, keys=[], mode='any'):
    ''' Returns all the hero abilities.

        Args:
            dict_ (dict): dictionary to search keywords in
            keys (list): words to be find in skills
            mode (str): 'all' or 'any' defines which keywords
                should be found in key for him to added to result

        Returns:
            abilities_ (list): list of Ability
    '''

    if len(keys) == 0:
        logging.warning('Please, provide `keys` for filter() function.')
        return

    properties = dict()
    for key, value in dict_.items():
        if mode == 'any':
            props = find_properties_any(value, keys)
            if len(props) == 0:
                continue
            properties[key] = {p[0]: p[1] for p in props}

    return properties


def find_properties_any(dict_, keywords=[]):
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

if __name__ == '__main__':
    data = abilities.main()
    # print(json.dumps(data, indent=2))
    p = find_properties(data, keys=['min', 'max'])
    # p = abilities.min_max2avg(data)
    print(json.dumps(p, indent=2))
