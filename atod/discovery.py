''' Set of functions which help to understand data and see what can be
    cleaned.
    In future this file would provide functions to take a look at the overall
    data, for example amount of abilities, heroes...
'''

from atod import Abilities


def check():
    a = Abilities.all()
    texts = a.get_texts()
    print(texts.shape)


if __name__ == '__main__':
    check()
