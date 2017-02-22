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


# TODO: check if return write_to is needed
def write_on_stack(write_to, path, key, value):
    ''' Writes values to the `result` dict.

        DFS kind of stack is used to define current level of depth of reading
        and writing into the dictionary, that's why function has such name.
        If the path is not completed yet, instead of throwing KeyError
        function will create missing dictionaries.

        :Args:
            path (array of str) : sequence of dict keys, defining where to
                                  write next value
            write_to (dict)     : result of parse function in which would be
                                  written key and value
            key (str)           : to this key would be written value
            value (str)         : value to write

        :Returns:
            write_to (dict) : changed write_to argument
    '''
    current = write_to
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

    return write_to


def remove_nt(input_str):
    ''' Returns string without tabs, line terminators and spaces. '''
    clean = input_str.replace(' ', '')
    clean = clean.replace('\t', '')
    clean = clean.replace('\n', '')

    return clean


def parse(filename):
    ''' Extracts the dict from unix-dialect txt file.

        First, it cleans the row - removes all the tabs and line terminators.
        Second, it splits string by " to get all values in the list
        Third, it cleans string from comments and empty strings created by
        split().
        After that, based on the length of cleaned row list, func defines is it
        the key, bracers or key with value and performs appropriate action.
    '''
    result = {}
    keys_stack = []
    with open(filename, 'r') as fp:
        for row in fp:
            # clean_ is a list without \t \n or spaces in it splitted by "
            clean_ = remove_nt(row).split('"')

            # remove all the comments and empty strings
            clean = [c for c in clean_ if '//' not in c and c != '']

            # if this is one
            if len(clean) == 1:
                # if this isn't bracers - this is the key
                if '{' not in clean and '}' not in clean:
                    # add the key to the stack
                    keys_stack.append(clean[0])

                if '}' in clean:
                    # pop key from the stack, since corresponding dictionary
                    # ended
                    keys_stack.pop()


            if len(clean) == 2:
                write_on_stack(write_to=result,
                               path=keys_stack,
                               key=clean[0],
                               value=clean[1]
                               )

    return result


# TODO: add check for .json in output
def to_json(input_filename=None, output_filename=None):
    ''' Saves parsed by parse() file in *.json.

        :Args:
            input_filename (str) : .txt file in unix-dialect from dota folder
            output_filename(str) : .json file to dump result dict

        :Returns:
            result (dict) : dict parsed by parse()
    '''
    # if input file is not provided nor as cl argument nor as func argument
    if not input_filename:
        print('Please, provide filename.')
        return

    result = parse(input_filename)

    # if output filename is not provided
    if not output_filename:
        # create a path for parsed file:
        # DATA_FOLDER/<inputfile_no_extension>.json
        output_filename = input_filename.split('.')[0] + '.json'

    with open(output_filename, 'w+') as fp:
        json.dump(result, fp, indent=4)

    return result


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
        data = json.load(fp)
        global_key = list(data.keys())[0]
        data = data[global_key]

    for in_game_name, description in data.items():
        tmp = {}
        for key in scheme.keys():
            try:
                tmp[key] = description[key]
            # hero_base doesn't have some fields
            except KeyError as e:
                tmp[key] = None
            # there are some non hero fields causes this
            except TypeError as t:
                pass

        if len(tmp) > 0:
            print(tmp)
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
    inp = v['input'][0] if v['input'] else None
    out = v['output'][0] if v['output'] else None
    to_json(input_filename=inp, output_filename=out)
