''' Set of functions which help to understand data and see what can be
    cleaned.
    In future this file would provide functions to take a look at the overall
    data, for example amount of abilities, heroes...
'''

from atod import Abilities, Hero


def check():
    a = Hero(15, 25) # this is Razor
    print(a.get_description())


if __name__ == '__main__':
    check()
