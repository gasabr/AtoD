#!/usr/bin/env python
import json
import pandas

import settings

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
print(items.shape)
print(items.loc[['item_veil_of_discord']]['phase_duration'])
items.set_value('item_veil_of_discord', 'phase_duration', 11)
print(items.loc[['item_veil_of_discord']]['phase_duration'])

# fill the pandas DataFrame about items
def fill_table():
    for key, item in items_data['DOTAAbilities'].items():
        if not 'recipe' in key:
            items_list.add(key)

            try:
                item_specials = item['AbilitySpecial']
                for key_, special in item_specials.items():
                    # print('wwfgchvbjknmlgcvhbjnkmlcgvhbjnkm')
                    for k, v in special.items():
                        if k == 'resist_debuff':
                            print(key)
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
print(list(items))
