#!/usr/bin/env python3
''' Set of functions to transform dict (json) to pandas.DataFrame. '''
import pandas


def create_numeric(data, rows, columns):
    ''' Creates part from numeric variables in binary vectors DataFrame. '''
    # DataFrame(abilities X effects)
    numeric = pandas.DataFrame([], index=rows, columns=columns)
    # TODO: logger.info('DataFrame with abilities created',
    #       'shape={}'.format(frame.shape))

    # fill DataFrame
    for key, values in numeric.iterrows():
        for e in list(values.index):
            # if this effect is inside any key of the ability
            values[e] = 1 if any(map(lambda k: e in k, data[key].keys())) else 0

    return numeric


def create_categorical(data, rows, columns):
    ''' Creates part from categorical variables in binary vectors DataFrame. '''
    # categorical features in ability description
    categorical = pandas.DataFrame([], index=rows, columns=columns)

    # fill categorical_part
    for skill, values in categorical.iterrows():
        categorical.loc[skill] = categorical.loc[skill].fillna(value=0)
        # for all the categorical variables
        for cat_var in columns:
            try:
                # check if this ability has such categorical variable
                getattr(data[skill], cat_var)
            except AttributeError as e:
                continue

            cat_values = data[skill][cat_var].split(' | ')

            if len(cat_values) == 1:
                column_to_write = '{}={}'.format(cat_var, cat_values[0])
                categorical.loc[skill][column_to_write] = 1
            else:
                for c in cat_values:
                    categorical.loc[skill]['{}={}'.format(cat_var, c)] = 1

    return categorical


def lists_to_mean(dict_):
    ''' Changes all the lists to their mean. '''
    for key in dict_.keys():
        if isinstance(dict_[key], list):
            dict_[key] = sum(dict_[key])/len(dict_[key])
        if isinstance(dict_[key], dict):
            lists_to_mean(dict_[key])

    return
