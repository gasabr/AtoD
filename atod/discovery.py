''' Set of functions which help to understand data and see what can be
    cleaned.
    In future this file would provide functions to take a look at the overall
    data, for example amount of abilities, heroes...
'''

from atod import Abilities


def check_models():
    abilities = Abilities.all()
    abilities.get_specs_list().shape


if __name__ == '__main__':
    check_models()
