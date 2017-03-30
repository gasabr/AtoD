from atod import settings
from atod.utils.db import to_rows
from atod.models.hero import HeroModel
from atod.models.item import ItemModel
from atod.utils.db.setup import session
from atod.utils.db.create_scheme import create_abilities_scheme


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
    rows = to_rows.json_to_rows(settings.ABILITIES_LISTS_FILE, scheme)
    print(rows)


if __name__ == '__main__':
    fill_abilities()
