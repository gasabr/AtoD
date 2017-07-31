''' Set of functions which help to understand data and see what can be
    cleaned.
    In future this file would provide functions to take a look at the overall
    data, for example amount of abilities, heroes...
'''

from atod import Hero
from atod.utils.pick import get_recommendations


if __name__ == '__main__':
    request = {
        'ban': ['bane', 'slark', 'lina', 'meepo'],
        'pick': ['elder_titan', 'alchemist'],
        'against': ['axe', 'phoenix']}

    a = get_recommendations(**request)
    print(a)
