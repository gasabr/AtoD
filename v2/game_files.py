#!/usr/bin/env python3
import config
import sys
import json


result = {}


def write_on_stack(path, key, value):
    ''' Writes values to the `result` dict.

        DFS kind of stack is used to define current level of depth of reading
        and writing into the dictionary, that's why function has such name.
        If the path is not completed yet, instead of throwing KeyError
        function will create missing dictionaries.

        :Args:
            path (array of str): sequence of dict keys, defining where to write
                                 next value
            value (array of str): [key, value, probably comments]
    '''
    current = result
    for p in path:
        try:
            current = current[p]
        except KeyError as e:
            current[p] = {}
            current = current[p]
    try:
        current[p][key] = value
    except KeyError as e:
        current[key] = value


filename = config.DATA_FOLDER + '/from-game/npc_heroes.txt'

# def parse(filename):
with open(filename, 'r') as fp:
    keys_stack = [] # stack of keys

    for row in fp:
        # split string to skip tabs and lineterminators
        splitted_t = row[:-1].split('\t')

        # delete all empty string in tabs splitted array
        clean_t = [s for s in splitted_t if s != '']

        try:
            # if this row is comment line
            if clean_t[0].startswith('//'):
                continue
        # TODO: check if except block is needed
        except IndexError as e:
            pass

        # it's a key for dictionary or one of the '{', '}'
        if len(clean_t) == 1:
            # it's the key
            if '{' not in clean_t and '}' not in clean_t:
                # add the key to the stack
                keys_stack.append(clean_t[0][1:-1])

            if '}' in clean_t:
                # pop key from the stack, since corresponding dictionary is read
                keys_stack.pop()

        # value is found
        if len(clean_t) >= 2:
            # extract strings from all-quotes style to list
            cleaned_attribute = list(map(lambda x: x[1:-1], clean_t[:2]))

            # pass them as key and value to the write function
            write_on_stack(path=keys_stack,
                           key=cleaned_attribute[0],
                           value=cleaned_attribute[1]
                       )

print(json.dumps(result['DOTAHeroes']['npc_dota_hero_base'], indent=2))


# Interface: from parse_game_files import parse_and_write()
