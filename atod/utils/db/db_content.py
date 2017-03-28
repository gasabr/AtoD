from atod import settings
from atod.models.hero import HeroModel
from atod.models.item import ItemModel
from atod.utils.db import to_rows
from atod.utils.db.setup_db import session


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
            # print(row)
            session.add(item)
            session.commit()
            unique_ids.add(row['ID'])


def fill_abilities():
    ''' FIlls abilities table with the data from cleaned abilities file. '''
    pass


if __name__ == '__main__':
    fill_heroes()
    fill_items()
