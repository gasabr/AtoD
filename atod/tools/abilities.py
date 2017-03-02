#!/usr/bin/env python3
''' Set of functions to work with npc_abilities.json'''
import os
import json

from atod import settings
# IDEA: move all from this import to this file
from atod.tools.json2vectors import get_keys, make_flat_dict


def count_keywords():
    with open(settings.ABILITIES_FILE, 'r') as fp:
        data = json.load(fp)['DOTAAbilities']

    keys = get_keys(data)
    which_ability = create_which_ability(data)

    print(len(which_ability))


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


if __name__ == '__main__':
    count_keywords()
