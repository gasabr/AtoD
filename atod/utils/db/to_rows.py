''' This file serves db_content.py  '''
import os
import json

from atod import settings


def heroes_file_to_rows(filename, scheme):
    ''' Gets the data from json files according to given db scheme.

        Idea: json file contents a lot of information that i don't need in db,
        so this function parses file to get the needed attributes.

        Args:
            filename (str) - name of json file to parse
            scheme (list of str) - fields what should be extracted from file

        Returns:
            rows (list of dicts) - dict there scheme elements are keys
    '''
    rows = []
    with open(filename, 'r') as fp:
        data = json.load(fp)['DOTAHeroes']

    for in_game_name, description in data.items():
        if in_game_name == 'Version' or 'hero_base' in in_game_name\
                or not 'url' in description:
            continue

        tmp = dict()
        tmp['in_game_name'] = in_game_name.split('npc_dota_hero_')[1]
        tmp['name'] = description['url']
        del description['url']

        # add name aliases
        try:
            tmp['aliases'] = description['NameAliases']
        except KeyError:
            tmp['aliases'] = None

        # add all over keys
        for key in scheme.keys():
            if key in tmp:
                continue

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


def ability_to_row(skills, schema):
    ''' Transforms ability description to database row. '''
    base = dict()
    with_list_values = dict()
    for k, v in skills.items():
        if isinstance(v, list):
            with_list_values[k] = v
        else:
            base[k] = v

    for col in schema:
        if col not in base and col not in with_list_values:
            base[col] = None

    if len(with_list_values) != 0:
        max_lvl = max([len(v) for _, v in with_list_values.items()])

        lvl_part = dict()
        for lvl in range(max_lvl):
            for k, v in with_list_values.items():
                lvl_part[k] = v[lvl] if lvl < len(v) else v[-1]

            # TODO: why should I use copy here?
            result = base.copy()
            for k, v in lvl_part.items():
                result[k] = v
            result['lvl'] = lvl + 1

            yield result

    else:
        base['lvl'] = 1
        yield base


def parse_skill_name(skill, heroes):
    ''' Splits skill name form game to hero name and skill name.
    
        In-game files store skills names as <hero>_<skill>, this function
        parses this representation to the names of the hero and of the skill.
        
        Args:
            skill (str): skills names from in-game files
            heroes (list of strings): heroes name in-game
            
        Returns:
            parsed (hero, skill_name):
    '''

    for hero in heroes:
        parts = skill.partition(hero)
        if hero in skill and parts[0] == '':
            return parts[1], parts[2].lstrip('_')

    return ()


def binarize_labels(labels, schema):
    ''' Binarize abilities labels.
    
        Creates a dictionary which maps schema to labels, fills unmarked
        labels with 0.
    
        Args:
            labels (iterable): numbers of marked labels
            schema (iterable): keys in result dictionary
            
        Returns:
            binary (dict): mapping of schema to labels
    '''

    binary = dict()
    for i, label in enumerate(schema):
        binary[label] = 1 if i+1 in labels else 0

    return binary