#!/usr/bin/env python3
''' Set of functions to work with npc_abilities.json'''
import json

from atod import settings
# IDEA: move all from this import to this file
from atod.tools.json2vectors import (make_flat_dict, create_encoding,
                                     find_heroes_abilities, find_all_values)


def count_keywords():
    with open(settings.ABILITIES_FILE, 'r') as fp:
        data = json.load(fp)['DOTAAbilities']

    heroes_abilities_list = find_heroes_abilities(data)

    heroes_abilities = {}
    for ability in heroes_abilities_list:
        heroes_abilities[ability] = data[ability]

    which_ability = create_which_ability(heroes_abilities)

    label(heroes_abilities)


def label(abilities):
    print('LABEL')
    labels = {}
    for ability, parameters in abilities.items():
        labels[ability] = []
        parameters = make_flat_dict(parameters)
        for p in parameters.keys():
            if 'lifesteal' in p or 'vampiric' in p or 'leech' in p:
                labels[ability].append('stun')

    for ability, categories in labels.items():
        if len(categories) >= 1:
            print(ability)


def create_which_ability(abilities):
    ''' Creates mapping from effect to abilities where it occurs. '''
    which_ability = {}
    for ability, parameters in abilities.items():
        if isinstance(parameters, dict):
            flat_parameters = make_flat_dict(parameters)
        else:
            continue

        for p in flat_parameters.keys():
            try:
                which_ability[p].append(ability)
            except KeyError as e:
                which_ability[p] = [ability]

    return which_ability


def get_encoding():
    '''Returns encoding of categorical features in abilities file. '''
    with open(settings.ABILITIES_FILE, 'r') as fp:
        abilities = json.load(fp)['DOTAAbilities']

    values = find_all_values(abilities)
    encoding = create_encoding(values)

    return encoding


if __name__ == '__main__':
    count_keywords()
