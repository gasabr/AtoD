#!/usr/bin/env python3
''' Set of functions to work with npc_abilities.json'''
import json
import pandas

from atod import settings
from atod.preprocessing.dictionary import make_flat_dict


def encode_effects(data, rows, columns):
    ''' Creates part from numeric variables in binary vectors DataFrame. '''
    # DataFrame(abilities X effects)
    effects = pandas.DataFrame([], index=rows, columns=columns)
    # TODO: logger.info('DataFrame with abilities created',
    #       'shape={}'.format(frame.shape))

    # fill DataFrame
    for key, values in effects.iterrows():
        for e in list(values.index):
            # if this effect is inside any key of the ability
            values[e] = 1 if any(map(lambda k: e in k, data[key].keys())) else 0

    return effects


def fill_numeric(data, rows, columns):
    numeric = pandas.DataFrame([], index=rows, columns=columns)

    for key, values in numeric.iterrows():
        for e in list(values.index):
            if e in data[key]:
                values[e] = data[key][e]

    return numeric


def create_categorical(data, rows, columns):
    ''' Creates part from categorical variables in binary vectors DataFrame. '''
    # categorical features in ability description
    categorical = pandas.DataFrame([], index=rows, columns=columns)

    # fill categorical_part
    for skill, values in categorical.iterrows():
        categorical.loc[skill] = categorical.loc[skill].fillna(value=0)
        for column in columns:
            var, value = column.split('=')[0], column.split('=')[1]
            if var in data[skill].keys() and value in data[skill][var]:
                categorical.loc[skill][column] = 1

    return categorical


def label(abilities):
    '''Just testing.'''
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


def add_labels():
    with open(settings.TMP_ABILITIES, 'r') as fp:
        labeled = json.load(fp)

    with open(settings.ABILITIES_LISTS_FILE, 'r') as fp:
        clean = json.load(fp)

    for ability, description in clean.items():
        if ability in labeled and 'labels' in labeled[ability]:
            clean[ability]['labels'] = labeled[ability]['labels']
        else:
            clean[ability]['labels'] = []

    with open(settings.ABILITIES_LISTS_LABELED_FILE, 'w+') as fp:
        json.dump(clean, fp, indent=2)