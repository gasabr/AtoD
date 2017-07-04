''' Set of functions which help to understand data and see what can be
    cleaned.
    In future this file would provide functions to take a look at the overall
    data, for example amount of abilities, heroes...
'''

from atod import Hero


if __name__ == '__main__':
    am = Hero(1)
    am.get_description(['laning'])
