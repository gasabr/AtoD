''' Set of functions which help to understand data and see what can be
    cleaned.
    In future this file would provide functions to take a look at the overall
    data, for example amount of abilities, heroes...
'''

from atod import Match
from atod.db import session
from atod.models import HeroModel


if __name__ == '__main__':
    match_id = 1000193456
    match = Match(match_id)
    print(match.radiant.get_summary().shape)
