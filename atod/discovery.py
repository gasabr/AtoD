''' Set of functions which help to understand data and see what can be
    cleaned.
    In future this file would provide functions to take a look at the overall
    data, for example amount of abilities, heroes...
'''

from atod.db.content import create_and_fill_abilities_texts


def check():
    create_and_fill_abilities_texts()


if __name__ == '__main__':
    check()
