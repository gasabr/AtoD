#!/usr/bin/env python3
''' Set of functions to work with the Dota2 internal files.

    - to_json() converts .txt in unix dialect to json
    - parse() performs actual parsing
    - clean_value() checks data types in values and returns appropriate
    - write_on_stack() to avoid recursion when writing to a dictionary
    - clean_nt() cleans tabs and line terminators from string
'''
import re
import argparse


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


def _clean_value(string):
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
        except ValueError:
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
def _write_on_stack(write_to, path, key, value):
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
        except KeyError:
            current[p] = dict()
            current = current[p]

    current[key] = value

    return current


def _parse(filename):
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
            dict           : JSON serializable dictionary created from given 
                            file
    '''

    result = {}
    keys_stack = []

    with open(filename, 'r', encoding='utf-8') as fp:
        for row in fp:
            # if string contain line separators inside value
            # this case was noticed only in `dota_english.txt`
            if row.count('"') == 3:
                row = row[:-1] + ' '
                next_row = next(fp)[:-1] + ' '
                while '"' not in next_row:
                    row += next_row
                    next_row = next(fp)

                row += next_row

            # cleaned_row is a list without \t \n or spaces in it
            cleaned_row = row.replace('\t', '').replace('\n', '')

            # remove comments
            if cleaned_row.startswith('//'):
                continue

            # remove all the comments and empty strings
            values = re.findall(r'"([\S| ]*?)"', cleaned_row)

            # if this is a key or a bracket
            if len(values) <= 1:
                # if this isn't bracers - this is the key
                if len(values) == 1:
                    # add the key to the stack
                    keys_stack.append(values[0])

                elif '}' in cleaned_row:
                    # pop key from the stack, since corresponding dictionary
                    # ended
                    keys_stack.pop()

            elif len(values) == 2:
                _write_on_stack(write_to=result,
                                path=keys_stack,
                                key=values[0],
                                value=_clean_value(values[1]))

    return result


def to_json(input_filename=None):
    ''' Wrapper for _parse() function.

        Args:
            input_filename (str) : .txt file in unix-dialect from dota folder

        Returns:
            result (dict) : dict parsed by parse()
    '''

    # if input file is not provided nor as cl argument nor as func argument
    if not input_filename:
        print('Please, provide filename.')
        return

    result = _parse(input_filename)

    return result


if __name__ == '__main__':
    inp = '/Users/gasabr/AtoD/atod/data/raw/dota_english.txt'
    to_json(input_filename=inp)
