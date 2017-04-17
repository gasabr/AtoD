''' Set of functions which help to understand data and see what can be
    cleaned.
    In future this file would provide functions to take a look at the overall
    data, for example amount of abilities, heroes...
'''

import json

from atod import settings
from atod.heroes import Hero, Heroes
from atod.preprocessing import dictionary, clean_abilities
from atod.preprocessing.abilities import abilities as Abilities
from atod.abilities import Abilities


def print_keys_occurrences():
    data = clean_abilities.clean()
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


def find_deprecated_skills():
    ''' If a hero has more than 4 skills in clean_abilities shows them.'''
    with open(settings.CONVERTER, 'r') as fp:
        converter = json.load(fp)

    n_heroes = 115
    for id_ in range(1, n_heroes + 1):
        try:
            h = Hero(converter[str(id_)])
        # 24 id is not used
        except KeyError:
            pass
        if len(h.abilities) > 4:
            print(h.abilities)
            print('------------')


def get_labeled():
    ''' Prints how much abilities are labeled. '''
    with open(settings.TMP_ABILITIES, 'r') as fp:
        in_process = json.load(fp)

    labeled = 0

    for ability, description in in_process.items():
        if 'labels' in description:
            labeled += 1

    return '{}/{} abilities are labeled'.format(labeled, len(in_process))


def check_heroes():
    heroes = []
    for id_ in [1, 2, 3, 4, 5]:
        heroes.append(Hero(id_))

    # h = Heroes(heroes)
    h = Hero(20)
    print(h.abilities.to_dataframe())


if __name__ == '__main__':
    check_heroes()
