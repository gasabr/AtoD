import json

from atod import files
from atod.db import schemas, session, create_tables
from atod.preprocessing import txt2json, json2rows, abilities
from atod.preprocessing.dictionary import get_str_keys
from atod.models import HeroModel, AbilitySpecsModel, AbilityModel


def create_and_fill_heroes():
    ''' Fills heroes table with the data from npc_heroes.json. '''
    heroes_file = files.get_heroes_file()

    heroes_dict = txt2json.to_json(heroes_file)

    rows = json2rows.heroes_to_rows(heroes_dict,
                                    schemas.get_hero_schema())

    for row in rows:
        hero = HeroModel(row)
        session.add(hero)

    create_tables.create_tables()
    session.commit()


# def fill_items():
#     '''Fills items table with the data from items.json.'''
#     rows = json2rows.items_file_to_rows(settings.ITEMS_FILE,
#                                         schemas.get_item_schema())
#     unique_ids = set()
#
#     for row in rows:
#         if row['ID'] not in unique_ids:
#             item = ItemModel(row)
#             session.add(item)
#             unique_ids.add(row['ID'])
#
#     session.commit()


def create_and_fill_abilities_specs():
    ''' FIlls table with the data from cleaned npc_abilities file. '''
    raw_file = files.get_abilities_file()
    parsed   = txt2json.to_json(raw_file)
    clean    = abilities.get_cleaned_abilities(parsed)

    schema = schemas.get_ability_specs_schema()

    # with open(settings.ABILITIES_LISTS_FILE, 'r') as fp:
    #     skills = json.load(fp)

    with open(files.get_converter_file(), 'r') as fp:
        converter = json.load(fp)

    heroes = get_str_keys(converter)

    for skill, description in clean.items():
        try:
            hero, skill_name = json2rows.parse_skill_name(skill, heroes)
        # if skill name cannot be parsed
        except ValueError:
            continue

        for row in json2rows.ability_to_row(description, schema):
            row['HeroID'] = converter[hero]
            row['name'] = skill_name
            row['pk'] = str(row['ID']) + '.' + str(row['lvl'])

            skill = AbilitySpecsModel(row)
            session.add(skill)

    # creates tables *if needed*
    create_tables.create_tables()
    session.commit()


def create_and_fill_abilities():
    ''' Fills abilities table'''

    with open(files.get_labeled_abilities_file(), 'r') as fp:
        skills = json.load(fp)

    # TODO: create converter table in db instead of it
    with open(files.get_converter_file(), 'r') as fp:
        converter = json.load(fp)

    # get hero to id converter
    heroes = get_str_keys(converter)

    for skill, description in skills.items():
        if 'special' in skill:
            continue

        # get skill and hero names
        try:
            hero, skill_name = json2rows.parse_skill_name(skill, heroes)
        except ValueError:
            continue

        # FIXME: using schemas.LABELS is not the right approach
        # binarize labels
        # for marked abilities
        if 'labels' in description:
            row = json2rows.binarize_labels(description['labels'],
                                            schemas.LABELS)
        # for unmarked abilities
        else:
            row = {k: 0 for k in schemas.LABELS}

        row['HeroID'] = converter[hero]
        row['name'] = skill_name
        row['ID'] = description['ID']

        skill = AbilityModel(row)
        session.add(skill)

    create_tables.create_tables()
    session.commit()


def create_and_fill_all():
    ''' Creates *all* tables and fills them with data. 
    
        Notes:
            * There is no list of tables, so tables are created by functions
            calls.
    '''

    create_and_fill_heroes()
    create_and_fill_abilities()
    create_and_fill_abilities_specs()

    # TODO: write logger message


if __name__ == '__main__':
    create_and_fill_all()
