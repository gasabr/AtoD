''' Set of functions which help to understand data and see what can be
    cleaned.
    In future this file would provide functions to take a look at the overall
    data, for example amount of abilities, heroes...
'''

from atod.db import content


if __name__ == '__main__':
    # content.add_heroes('/Users/gasabr/AtoD/atod/data/706f/npc_heroes.txt',
    #                    '706f')
    content.add_abilities_texts('/Users/gasabr/AtoD/atod/data/706f/dota_english.txt',
                          patch='706f')

