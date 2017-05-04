''' Set of functions which help to understand data and see what can be
    cleaned.
    In future this file would provide functions to take a look at the overall
    data, for example amount of abilities, heroes...
'''

from atod import Abilities, Hero
from atod.db import session
from atod.models import HeroModel


def check():
    a = Hero(15, 25) # this is Razor
    print(a.get_hero_type())


def get_all_types():
    query = session.query(HeroModel.HeroType).all()
    types = set([t[0] for t in query if t[0] is not None])
    types = set([r for t in types
                   for r in t.split(' | ')])

    print(types)


if __name__ == '__main__':
    check()
