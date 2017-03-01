#!/usr/bin/env python
import json
import pandas

import settings

# TODO write docstring or delete this function
def pop_features():
    filename = settings.DATA_FOLDER + 'from-game/items.json'
    items = {}
    with open(filename, 'r') as fp:
        items_data = json.load(fp)

    basic_features = set()
    items_list = set()

    # get all possible items features
    for key, item in items_data['DOTAAbilities'].items():
        if not 'recipe' in key:
            items_list.add(key)

            try:
                item_specials = item['AbilitySpecial']
                for key_, special in item_specials.items():
                    for k in special.keys():
                        basic_features.add(k)
            # there is Version key which doesn't content needed keys
            except AttributeError as e:
                continue
            # recipes will go here
            except KeyError as e:
                continue
            except TypeError as e:
                continue

    items = pandas.DataFrame([], index=items_list, columns=basic_features)

    # fill the pandas DataFrame about items
    def fill_table():
        for key, item in items_data['DOTAAbilities'].items():
            if not 'recipe' in key:
                items_list.add(key)

                try:
                    item_specials = item['AbilitySpecial']
                    for key_, special in item_specials.items():
                        for k, v in special.items():
                            items.set_value(key, k, v)
                # there is Version key which doesn't content needed keys
                except AttributeError as e:
                    continue
                # recipes will go here
                except KeyError as e:
                    continue
                except TypeError as e:
                    continue

    fill_table()

    print(len(basic_features))
    print(len(items_list))
    veil = items.loc[['item_hand_of_midas']]['resist_debuff']

    # items with popular features
    items = items.dropna(1, thresh=4)
    items = items.dropna(0, 'all')
    print(items.columns)


def get_similar_effects():
    ''' Finds similar features.

        There are a lot of skills with similar effects: stuns, heals...
        but their effects stored in different variables inside attributes file.
        This function is aimed to collect effects by similarity in the name.
        This function was written to understand data better, it's not used
        anywhere.
    '''
    abilities = to_vectors(settings.ABILITIES_FILE).T

    print(abilities.index)

    # drop all the scepter effects
    effects_list = [e for e in list(abilities.columns) if 'scepter' not in e]

    heal_words = ['heal', 'restore', 'hp', 'regen']

    damage_effects  = [e for e in effects_list if 'damage' in e and
                       'illusion' not in e and 'replica' not in e]
    move_effects    = [e for e in effects_list if 'move' in e]
    healing_effects = [e for e in effects_list if
                               any(map(lambda x: x in e, heal_words))]
    durations       = [e for e in effects_list if 'duration' in e]
    stuns           = [e for e in effects_list if 'stun' in e]
    # TODO: same for illusions, replicas
    # TODO: same for reductions, probably

    print(len(damage_effects))
    print(len(move_effects))
    print(len(healing_effects))
    print(len(durations))
    print(len(stuns))

    # FIXME: change this name to lowercase one
    D = abilities[damage_effects]
    D = D.dropna(1)
    D = D.dropna(0)

    print(D.shape)
