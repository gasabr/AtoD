#!/usr/bin/env python3
''' Set of functions to transform dict (json) to pandas.DataFrame. '''


def lists_to_mean(dict_):
    ''' Changes all the lists to their mean. '''
    for key in dict_.keys():
        if isinstance(dict_[key], list):
            dict_[key] = sum(dict_[key])/len(dict_[key])
        if isinstance(dict_[key], dict):
            lists_to_mean(dict_[key])

    return
