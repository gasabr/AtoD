#!/usr/bin/env python3
''' Set of functions to work with the Dota2 internal files

    - to_json() converts .txt in unix dialect to json
    - json_to_rows() converts .json to the dicts with respect to db scheme
'''
import json
import argparse
import os

from atod import settings

# Command line arguments parser
parser = argparse.ArgumentParser(
    description='Parser for Dota files in unix dialect'
)
parser.add_argument('--input',
                    nargs=1,
                    help='define input file'
                    )
parser.add_argument('--output',
                    nargs=1,
                    help='define output file (json)'
                    )
args = parser.parse_args()


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


def parse(filename):
    ''' Parses file with given name, writes result to `result` dictionary. '''
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
                # TODO: rewrite this part to be able to parse:
                # \t\t\t<space><space>"key"
                # if bad formatting
                if any(map(lambda x: ' ' in x, clean_t)):
                    key = clean_t[0].split(' ')[0]
                    value = clean_t[0].split(' ')[1]
                    # write_on_stack(path=keys_stack, key=key, value=value)
                    continue

                # it's the key
                if '{' not in clean_t and '}' not in clean_t:
                    # add the key to the stack
                    keys_stack.append(clean_t[0][1:-1])

                if '}' in clean_t:
                    # pop key from the stack, since corresponding dictionary
                    # ended
                    print(keys_stack)
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


def to_json(input_filename=None, output_filename=None):
    # if input file is not provided nor as cl argument nor as func argument
    global result
    result = {}

    if not input_filename:
        print('Please, provide filename.')
        return

    parse(input_filename)

    # if output filename is not provided
    if not output_filename:
        # create a path for parsed file:
        # DATA_FOLDER/<inputfile_no_extension>.json
        output_filename = input_filename.split('.')[0] + '.json'

    with open(output_filename, 'w+') as fp:
        json.dump(result, fp, indent=4)
        result = {}


def json_to_rows(filename, scheme):
    ''' Gets the data from json files according to given db scheme.

        Idea: json file contents a lot of information that i don't need in db,
        so this fuction parses file to get the needed attributes.

        :Args:
            filename (str) - name of json file to parse
            scheme (list of str) - fieds what should be extracted from file

        :Returns:
            rows (list of dicts) - dict there scheme elements are keys
    '''
    rows = []
    with open(filename, 'r') as fp:
        # TODO: get the only key not DOTAHeroes
        data = json.load(fp)
        global_key = list(data.keys())[0]
        data = data[global_key]

    for in_game_name, description in data.items():
        tmp = {}
        for key in scheme.keys():
            try:
                tmp[key] = description[key]
                print('tmp[key] =', description[key])
            # hero_base doesn't have some fields
            except KeyError as e:
                # print('Hero {} with does not have {} field'.format(
                #     in_game_name, key
                # ))
                tmp[key] = None
            # there are some non hero fields causes this
            except TypeError as t:
                pass

        if len(tmp) > 0:
            rows.append(tmp)

    return rows


def items_rows(filename, scheme):
    ''' Get rows for items table. '''
    rows = []
    with open(filename, 'r') as fp:
        # TODO: get the only key not DOTAHeroes
        data = json.load(fp)

    global_key = list(data.keys())[0]
    data = data[global_key]

    for in_game_name, description in data.items():
        tmp = {}
        print(in_game_name)
        for key in scheme.keys():
            try:
                tmp[key] = description[key]
                # print('tmp[{}] ='.format(key), description[key])
            # hero_base doesn't have some fields
            except KeyError as e:
                tmp[key] = None
            # there are some non hero fields causes this
            except TypeError as t:
                pass

        # extract specials
        try:
            specials = description['AbilitySpecial']
            for key, value in specials.items():
                for k, v in value.items():
                    if k != 'var_type':
                        tmp[k] = v
        except TypeError as e:
            print(description)
        except KeyError as e:
            pass

        for kk in tmp.keys():
            if kk not in scheme.keys():
                print('retard alert')

        if len(tmp) > 0:
            rows.append(tmp)

    return rows



def get_types(abilities):
    ''' Maps AbilitySpecial to type of this field.

        :Args:
            abilities (dict) - DOTAAbilities from items.json or npc_abilities

        :Returns:
            fields_types (dict) - mapping of field to its type
    '''
    fields_types = {}
    items_list = []
    for ability, properties in abilities.items():
        try:
            for key, value in properties['AbilitySpecial'].items():
                for k, v in value.items():
                    if key != 'var_type' and key:
                        fields_types[k] = value['var_type']
        # all the recipies will fall there
        except KeyError as e:
            pass
        except TypeError as e:
            pass

    return fields_types


def write_item_types():
    ''' Combines get_types() and settings.items_scheme in one file.

        :Returns:
            all_ (dict) = get_types() + settings.items_scheme
    '''
    DOTAAbilities = {}
    with open(settings.DATA_FOLDER + 'from-game/items.json') as fp:
        DOTAAbilities = json.load(fp)['DOTAAbilities']
    specials = get_types(DOTAAbilities)
    basics = settings.items_scheme

    all_ = {}
    for key, value in basics.items():
        all_[key] = value

    for key, value in specials.items():
        # TODO: move mapping to function if needed
        all_[key] = value

    filename = os.path.join(settings.DATA_FOLDER, 'items_types.json')
    with open(filename, 'w+') as fp:
        json.dump(all_, fp, indent=2)

    return all_


if __name__ == '__main__':
    v = vars(args)
    print(v['input'][0])
    inp = v['input'][0] if v['input'] else None
    out = v['output'][0] if v['output'] else None
    to_json(input_filename=inp, output_filename=out)