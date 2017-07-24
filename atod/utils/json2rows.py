''' This file serves db_content.py  '''
import json
from sqlalchemy.orm import sessionmaker, scoped_session

# this are for parse_skill_name()
from atod.db import engine
from atod.db_models.hero import HeroModel
from atod.utils import dictionary

session = scoped_session(sessionmaker(bind=engine))

# FIXME: write heroes_base_info table to fix note of parse_skill_name().


def heroes_to_rows(heroes_dict, schema):
    ''' Gets the data from json files according to given db scheme.

        Idea: json file contents a lot of information that I don't need in db,
        so this function parses file to get the needed attributes.

        Args:
            heroes_dict (dict)  : parsed to dict npc_heroes.txt
            schema (list of str): fields what should be extracted from file

        Yields:
            dict: where schema elements are keys
    '''

    data = heroes_dict['DOTAHeroes']

    for in_game_name, description in data.items():

        if in_game_name == 'Version' or 'hero_base' in in_game_name\
                or not 'url' in description:
            continue

        tmp = dict()
        tmp['in_game_name'] = in_game_name.split('npc_dota_hero_')[1]
        tmp['name'] = description['url'].replace('_', ' ')
        del description['url']

        # add name aliases
        try:
            tmp['aliases'] = description['NameAliases']
        except KeyError:
            tmp['aliases'] = None

        flat_description = dictionary.make_flat_dict(description)

        # add all over keys
        for key in schema:
            if key in tmp:
                continue

            try:
                tmp[key] = flat_description[key]
            # hero_base doesn't have some fields
            except KeyError:
                tmp[key] = None
            # there are some non hero fields causes this
            except TypeError:
                pass

        if len(tmp) > 0:
            yield tmp


# DEPRECATED IN CURRENT VERSION
def items_file_to_rows(filename, scheme):
    ''' Get rows for items table. '''

    with open(filename, 'r') as fp:
        data = json.load(fp)

    global_key = list(data.keys())[0]
    data = data[global_key]

    for in_game_name, description in data.items():
        if in_game_name == 'Version':
            continue

        tmp = dict()

        tmp['in_game_name'] = in_game_name.split('item_')[1]
        tmp['name'] = tmp['in_game_name'].replace('_', ' ').title()

        if 'ItemAliases' in description:
            tmp['aliases'] = description['ItemAliases']
        else:
            tmp['aliases'] = None

        for key in scheme.keys():
            try:
                tmp[key] = description[key]

            except KeyError:
                tmp[key] = None
            # there are some non hero fields causes this
            except TypeError:
                pass

        # extract specials
        try:
            specials = description['AbilitySpecial']
            for key, value in specials.items():
                for k, v in value.items():
                    if k != 'var_type':
                        tmp[k] = v
        except TypeError:
            print(description)
        except KeyError:
            pass

        for kk in tmp.keys():
            if kk not in scheme.keys():
                print('retard alert')

        if len(tmp) > 0:
            yield tmp


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
        except KeyError:
            pass
        except TypeError:
            pass

    return fields_types


def ability_to_row(description, schema):
    ''' Transforms ability description to database row.

        This function produce descriptions for all levels of ability from
        its description.

        Args:
            description (dict): mapping property of ability to its values
            schema (list of strings): fields that should be extracted from
                the description

        Yields:
            dict: mapping of properties to its values on some level. Level is
                added to result (as 'lvl' key).
    '''

    base = dict()
    with_list_values = dict()
    for k, v in description.items():
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


def parse_skill_name(skill):
    ''' Splits skill name from game to hero name and skill name.

        In-game files store skills names as <hero>_<skill>, this function
        parses this representation to the names of the hero and of the skill.

        Notes:
            For this function to work heroes table for current version should
            be created.

        Args:
            skill (str): skills names from in-game files

        Returns:
            parsed (hero, skill_name):
    '''

    heroes_names = [h[0] for h in session.query(HeroModel.in_game_name).all()]

    for hero in heroes_names:
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
