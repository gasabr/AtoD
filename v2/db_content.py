import settings
from setup_db import session
from dynamic_models import HeroModel
import game_files


def fill_heroes():
    ''' Fills heroes table with the data from npc_heroes.json. '''
    rows = game_files.json_to_rows(settings.HEROES_FILE, settings.heroes_scheme)

    for row in rows:
        print(row)
        hero = HeroModel(row)
        session.add(hero)
        session.commit()


if __name__ == '__main__':
    fill_heroes()
