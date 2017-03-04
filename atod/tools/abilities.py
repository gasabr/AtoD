#!/usr/bin/env python3
''' Set of functions to work with npc_abilities.json'''
import json

from atod import settings
from atod.tools.json2vectors import (make_flat_dict, create_encoding,
                                     find_all_values)

    
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

