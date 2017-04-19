#!/usr/bin/env python3
''' Set of functions to work with the Dota2 internal files.

    - to_json() converts .txt in unix dialect to json
    - parse() performs actual parsing
    - clean_value() checks data types in values and returns appropriate
    - write_on_stack() to avoid recursion when writing to a dictionary
    - clean_nt() cleans tabs and line terminators from string
'''
import re
import json
import argparse

from atod import settings

# Command line arguments parser
parser = argparse.ArgumentParser(
    description='Parser for Dota files in unix dialect')
parser.add_argument('--input',
                    nargs=1,
                    help='define input file')
parser.add_argument('--output',
                    nargs=1,
                    help='define output file (json)')
args = parser.parse_args()


def clean_value(string):
    ''' Transforms quoted value to the standard types.

        Strategy:
            "int" -> int
            "float" -> float
            "int int" -> [int int]
            "any string" -> string
        Check out test_data/numbers.json for examples

        Args:
            string (str) : value in parsed dictionary

        Returns:
            value (str/float/integer) : cleaned value
    '''
    # remove quotes
    # if the string is digit
    if string.strip('-f').replace('.', '', 1).isdigit():
        try:
            return int(string)
        except ValueError as e:
            if string[-1] == 'f':
                return float(string[:-1])
            else:
                return float(string)
    # else if string is a list of numbers
    elif all(map(lambda s: s.strip('-f').replace('.','',1).isdigit(),
                 string.split(' '))):
        array = [float(s) for s in string.split(' ')]
        return array

    # in other cases just return string
    return string


# TODO: check if return write_to is needed
def write_on_stack(write_to, path, key, value):
    ''' Writes values to the `result` dict.

        DFS kind of stack is used to define current level of depth of reading
        and writing into the dictionary, that's why function has such name.
        If the path is not completed yet, instead of throwing KeyError
        function will create missing dictionaries.

        Args:
            path (array of str) : sequence of dict keys, defining where to
                                  write next value
            write_to (dict)     : result of parse function in which would be
                                  written key and value
            key (str)           : to this key would be written value
            value (str)         : value to write

        Returns:
            write_to (dict) : changed write_to argument
    '''

    current = write_to
    # find or create the end destination for writing value
    for p in path:
        try:
            current = current[p]
        except KeyError as e:
            current[p] = {}
            current = current[p]
    # trying to write value in the end of stack
    try:
        current[p][key] = value
    except TypeError:
        print(path)
    except KeyError:
        current[key] = value

    return write_to


def remove_nt(input_str):
    ''' Returns string without tabs, line terminators and spaces. '''
    clean = input_str.replace('\t', '')
    clean = clean.replace('\n', '')

    return clean


def parse(filename):
    ''' Extracts the dict from unix-dialect txt file.

        First, it cleans the row - removes all the tabs and line terminators.
        Second, it checks if the string starts with // - if so, go next row.
        Third, it finds all the payload in string with regex and saves it
        into a list.
        After that, based on the length of cleaned row list, func defines is 
        it.
        the key, bracers or key with value and performs appropriate action.

        Args:
            filename (str) : file to parse

        Returns:
            result (dict) : JSON serializeble dictionary created from given 
                            file
    '''
    result = {}
    keys_stack = []
    with open(filename, 'r') as fp:
        try:
            for row in fp:
                # clean_ is a list without \t \n or spaces in it
                clean_ = remove_nt(row)

                # remove comments
                if clean_.startswith('//'):
                    continue

                # if string contain line separators inside value
                # this case noticed only in `dota_english.txt`
                if row.count('"') == 3:
                    while '"' not in next(fp):
                        row += next(fp)

                # remove all the comments and empty strings
                clean = re.findall(r'"([\S| ]*?)"', row)

                # if this is a key or a bracket
                if len(clean) <= 1:
                    # if this isn't bracers - this is the key
                    if len(clean) == 1:
                        # add the key to the stack
                        keys_stack.append(clean[0])

                    elif '}' in row:
                        # pop key from the stack, since corresponding dictionary
                        # ended
                        keys_stack.pop()

                elif len(clean) == 2:
                    write_on_stack(write_to=result,
                                   path=keys_stack,
                                   key=clean[0],
                                   value=clean_value(clean[1]))
        except UnicodeDecodeError:
            print(row)

    return result


# TODO: add check for .json in output
def to_json(input_filename=None, output_filename=None):
    ''' Saves parsed by parse() file in *.json.

        Args:
            input_filename (str) : .txt file in unix-dialect from dota folder
            output_filename(str) : .json file to dump result dict
                if output_filename == '' will write to the same folder and
                with the same name as input file.
                if None - won't write result to file
                (optional, default None)

        Returns:
            result (dict) : dict parsed by parse()
    '''
    # if input file is not provided nor as cl argument nor as func argument
    if not input_filename:
        print('Please, provide filename.')
        return

    result = parse(input_filename)

    # if output filename is not provided
    if output_filename is None:
        # create a path for parsed file:
        # DATA_FOLDER/parsed/<inputfile_no_extension>.json
        output_filename = input_filename.split('.')[0] + '.json'

    if output_filename:
        with open(output_filename, 'w+') as fp:
            json.dump(result, fp, indent=4)

    print(output_filename)

    return result


if __name__ == '__main__':
    inp = '/Users/gasabr/AtoD/atod/data/raw/dota_english.txt'
    to_json(input_filename=inp)
