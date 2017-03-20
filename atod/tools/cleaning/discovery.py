''' Set of functions which help to understand data and see what can be
    cleaned.
'''

import json
import logging

from atod.tools import dictionary
from atod.tools.cleaning import abilities
from atod.tools.dictionary import all_keys

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


if __name__ == '__main__':
    data = abilities.clean()

    p = dictionary.find_keys(data, keywords=['armor'])
    c = dictionary.count_keys(data)
    print(c)

    count = {k: v for k, v in c.items() if k not in data.keys() and v == 1}
    print(type(count))

    # print(sorted(set(all_keys(data, include_dict_keys=False))))
    print(json.dumps(count, indent=2))
    print(len(count))
