import json

from atod.db import session

from atod import settings
from atod.db.schemas import create_abilities_scheme
from atod.models import HeroModel, ItemModel, AbilitySpecsModel, AbilityModel
from atod.preprocessing import json2rows
from atod.preprocessing.dictionary import get_str_keys


def fill_heroes():
    '''Fills heroes table with the data from npc_heroes.json.'''
    rows = json2rows.heroes_file_to_rows(settings.HEROES_FILE,
                                         settings.heroes_scheme)

    for row in rows:
        if 'HeroID' in row:
            hero = HeroModel(row)
            session.add(hero)
        else:
            raise KeyError(row['name'])

    session.commit()


def fill_items():
    '''Fills items table with the data from items.json.'''
    rows = json2rows.items_file_to_rows(settings.ITEMS_FILE, settings.items_scheme)
    unique_ids = set()

    for row in rows:
        if row['ID'] not in unique_ids:
            item = ItemModel(row)
            session.add(item)
            unique_ids.add(row['ID'])

    session.commit()


def fill_abilities_specs():
    ''' FIlls table with the data from cleaned npc_abilities file. '''
    schema = create_abilities_scheme()

    with open(settings.ABILITIES_LISTS_FILE, 'r') as fp:
        skills = json.load(fp)

    with open(settings.IN_GAME_CONVERTER, 'r') as fp:
        converter = json.load(fp)

    heroes = get_str_keys(converter)

    for skill, description in skills.items():
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

    session.commit()


def fill_abilities():
    ''' Fills abilities table'''

    with open(settings.ABILITIES_LISTS_LABELED_FILE, 'r') as fp:
        skills = json.load(fp)

    with open(settings.IN_GAME_CONVERTER, 'r') as fp:
        converter = json.load(fp)

    heroes = get_str_keys(converter)

    for skill, description in skills.items():
        # get skill and hero names
        try:
            hero, skill_name = json2rows.parse_skill_name(skill, heroes)
        except ValueError:
            continue

        if 'special' in skill:
            continue

        # binarize labels
        # for marked abilities
        if 'labels' in description:
            row = json2rows.binarize_labels(description['labels'],
                                            settings.LABELS)
        # for unmarked abilities
        else:
            row = {k: 0 for k in settings.LABELS}

        row['HeroID'] = converter[hero]
        row['name'] = skill_name
        row['ID'] = description['ID']

        skill = AbilityModel(row)
        session.add(skill)

    session.commit()


if __name__ == '__main__':
    fill_abilities()
