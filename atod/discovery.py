''' Set of functions which help to understand data and see what can be
    cleaned.
    In future this file would provide functions to take a look at the overall
    data, for example amount of abilities, heroes...
'''

from atod import Abilities, Hero
from atod.db import session
from atod.models import HeroModel


if __name__ == '__main__':
    for id_ in [1, 5, 28, 65, 12]:
        hero = Hero(id_)
        print(hero.name, list(hero.get_roles()))
