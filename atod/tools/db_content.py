from atod import settings
from atod.models import HeroModel, ItemModel
from atod.setup_db import session
from atod.tools.modeling import to_rows


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


if __name__ == '__main__':
    fill_heroes()
    fill_items()
