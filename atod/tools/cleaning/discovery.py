''' Set of functions which help to understand data and see what can be
    cleaned.
'''

import json

from atod.tools import dictionary
from atod.tools.cleaning import abilities
from atod.abilities import abilities as Abilities

def print_keys_occurrences():
    data = abilities.clean()
    key2occur = dictionary.count_keys(data)

    # remove abilities names from key2occur
    for ability_name in data:
        if ability_name in key2occur.keys():
            del key2occur[ability_name]

    keys_by_occur = sorted(key2occur, key=key2occur.get)
    for key in keys_by_occur:
        print(key, '->', key2occur[key])


def remove_single_vars():
    frame = Abilities.clean_frame
    print(list(frame.shape))
    # print(list(frame.ix[:,'arrow_count']))

if __name__ == '__main__':
    remove_single_vars()
