''' This file serves db_content.py  '''
import os
import json

from atod import settings

def json_to_rows(filename, scheme):
    ''' Gets the data from json files according to given db scheme.

        Idea: json file contents a lot of information that i don't need in db,
        so this function parses file to get the needed attributes.

        Args:
            filename (str) - name of json file to parse
            scheme (list of str) - fieds what should be extracted from file

        Returns:
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
            rows.append(tmp)

            if 'HeroID' not in tmp:
                print(tmp)

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

        Args:
            abilities (dict) - DOTAAbilities from items.json or npc_abilities

        Returns:
            fields_types (dict) - mapping of field to its type
    '''

    fields_types = {}
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

        Returns:
            all_ (dict) = get_types() + settings.items_scheme
    '''

    with open(settings.DATA_FOLDER + 'parsed/items.json') as fp:
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
