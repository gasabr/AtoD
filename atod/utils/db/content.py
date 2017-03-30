import json

from atod import settings
from atod.utils.db import to_rows
from atod.models import HeroModel, ItemModel, AbilityModel
from atod.utils.db.setup import session
from atod.utils.db.create_scheme import create_abilities_scheme
from atod.utils.dictionary import get_str_keys


def fill_heroes():
    '''Fills heroes table with the data from npc_heroes.json.'''
    rows = to_rows.json_to_rows(settings.HEROES_FILE, settings.heroes_scheme)

    for row in rows:
        if row['HeroID']:
            hero = HeroModel(row)
            session.add(hero)
            session.commit()


def fill_items():
    '''Fills items table with the data from items.json.'''
    rows = to_rows.items_rows(settings.ITEMS_FILE, settings.items_scheme)
    unique_ids = set()

    for row in rows:
        if row['ID'] not in unique_ids:
            item = ItemModel(row)
            session.add(item)
            session.commit()
            unique_ids.add(row['ID'])


def fill_abilities():
    ''' FIlls abilities table with the data from cleaned abilities file. '''
    scheme = create_abilities_scheme()

    with open(settings.ABILITIES_LISTS_FILE, 'r') as fp:
        skills = json.load(fp)

    with open(settings.IN_GAME_CONVERTER, 'r') as fp:
        converter = json.load(fp)

    heroes = get_str_keys(converter)

    for skill, description in skills.items():
        hero, skill_name = to_rows.parse_skill_name(skill, heroes)
        for row in to_rows.ability_to_row(description, scheme):
            row['HeroID'] = converter[hero]
            row['name'] = skill_name
            row['pk'] = str(row['ID']) + '.' + str(row['lvl'])

            skill = AbilityModel(row)
            session.add(skill)

    session.commit()


if __name__ == '__main__':
    fill_abilities()
