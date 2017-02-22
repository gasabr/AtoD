from atod import settings
from atod.setup_db import session
from atod.models import HeroModel, ItemModel
from atod.tools import game_files


def fill_heroes():
    ''' Fills heroes table with the data from npc_heroes.json. '''
    rows = game_files.json_to_rows(settings.HEROES_FILE, settings.heroes_scheme)

    for row in rows:
        hero = HeroModel(row)
        session.add(hero)
        # session.commit()


def fill_items():
    ''' Fills items table with the data from items.json. '''
    rows = game_files.items_rows(settings.ITEMS_FILE, settings.items_scheme)
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
    # fill_items()
