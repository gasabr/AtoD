
# coding: utf-8

import os
import json
import numpy as np
import pandas as pd
from itertools import combinations, product

from atod import Hero, Heroes, settings

n_heroes = 115

matches_file = os.path.join(settings.DATA_FOLDER, 'players_in_matches.json')
with open(matches_file, 'r') as fp:
    players_in_matches = json.load(fp)

# TODO:
# Print some info about dataset:
#  * first match date
#  * last match date
#  * number of matches

# TODO:
# def how_many_nans(X: pd.DataFrame) -> int:

matches = dict()

for record in players_in_matches:
    # create match in matches dictionary with arrays for
    # winners and losers ids
    matches.setdefault(str(record['match_id']),
                       {
                        'winners': [],
                        'loosers': [],
                       }
                      )
    if record['win']:
        # add hero to winners of this match
        matches[str(record['match_id'])]['winners'].append(record['hero_id'])
    else:
        # add hero to losers
        matches[str(record['match_id'])]['loosers'].append(record['hero_id'])

# length of matches should be 10 times smaller than length of players...
# since there are 10 players in each match
assert len(matches), len(players_in_matches) / 10



# crete and fill
# TODO: rename matrices
matches_together = np.zeros((n_heroes, n_heroes))
matches_won = np.zeros((n_heroes, n_heroes))
matches_lost = np.zeros((n_heroes, n_heroes))
matches_against = np.zeros((n_heroes, n_heroes))

for match in matches.values():
    # for winners
    # sorting is needed to have upper traingular matrix
    # combinations produces all heroes pairs with smaller id first
    for hero1, hero2 in combinations(sorted(match['winners']), 2):
        matches_together[hero1][hero2] += 1
        matches_won[hero1][hero2] += 1

    for hero1, hero2 in combinations(sorted(match['loosers']), 2):
        matches_together[hero1][hero2] += 1

    for looser, winner in product(match['loosers'], match['winners']):
        matches_against[looser][winner] += 1
        matches_against[winner][looser] += 1
        matches_lost[looser][winner] += 1



# minimum number of matches for pair of heroes to be included in dataset
min_matches_played = 10
max_winrate = .65
max_matches_together = max([max(a) for a in matches_together])
were_nulls = sum([a.shape[0] - np.count_nonzero(a) for a in matches_together])

# if combination of 2 heroes were used less than `min_matches` times,
# don't count their win(lose)rate (it would be NaN in result matrix)
matches_together[matches_together < min_matches_played] = np.NaN
matches_together[matches_together > max_winrate] = max_winrate
matches_against[matches_against < min_matches_played] = np.NaN

become_nulls = sum([a.shape[0] - np.count_nonzero(a) for a in matches_together])

print(become_nulls - were_nulls)

# find maximum amount of matches played by 2 heroes
max_matches_played = np.nanmax([np.nanmax(hero)
                                for hero in matches_together])

# some combinations were played more than another, so
# there is more confidence in picking this kind of heroes (tiny-wi)

winrate_ = (matches_won / matches_together) * (1 + matches_together / max_matches_played)
winrate = pd.DataFrame(winrate_)
winrate.dropna(axis=0, how='all', inplace=True)
winrate.dropna(axis=1, how='all', inplace=True)
winrate.head()

lose_rate_ = matches_lost / matches_against
lose_rate = pd.DataFrame(lose_rate_)
lose_rate.dropna(axis=0, how='all', inplace=True)
lose_rate.dropna(axis=1, how='all', inplace=True)
lose_rate.head()

n = winrate.shape[0]
# how many heroes pairs don't have enough matches to have
# meaningful winrate
n_bad_pairs = n**2 - winrate.count().sum() - (n**2 - n)/2
n_pairs = (n**2 - n)/2
print('Percent of pairs with not enough matches to count them:',
      n_bad_pairs / n_pairs)

def _get_recommendation(pick, against=[], ban=[]):
    ''' Finds the next best hero for already `picked`.

    Notes:
        - All arguments are lists of heroes names. Names should be valid
        arguments for Hero.from_name().
        - Order in returned value is important: closer hero to the start -
        better it is as a pick.

    Args:
        pick (list)   : already picked heroes
        againts (list): heroes against which pick is playing
        ban (list)    : heroes that cannot be used

    Returns:
        str: name of the best hero to pick given allies, banned heroes and
            opponents.
    '''

    best_connection = -100
    next_pick = 0

    # transform lists of names to the lists of ids
    pick_ids = list(Heroes.from_names(pick).get_ids())
    ban_ids  = list(Heroes.from_names(ban).get_ids())
    against_ids = list(Heroes.from_names(against).get_ids())

    for next_hero_id in winrate.index:
        # if this hero is not in the opening
        if next_hero_id not in pick_ids and next_hero_id not in ban_ids \
                and next_hero_id not in against_ids:

            total_connection = 0
            for picked_hero in pick_ids:
                hero1, hero2 = sorted([next_hero_id, picked_hero])
                total_connection += winrate.loc[hero1][hero2]

            for enemy in against_ids:
                total_connection -= lose_rate.loc[next_hero_id][enemy]

            if total_connection > best_connection:
                best_hero = next_hero_id
                best_connection = total_connection

    best_hero_name = Hero(best_hero.item()).name
    return best_hero_name


def get_recommendations(pick, against=[], ban=[]):
    ''' Chooses 5 best heroes to add to the `pick`.

    Args:
        pick (list): heroes to which next one should be recommended
        against (list) (optional, default=[]): list of heroes against which
            `pick` heroes are going to play
        ban (list) (optional, default=[]): banned heroes.

    Returns:
        (list): heroes that will fit the best for the next pick for `pick`.
    '''
    recommendations = []
    while (len(recommendations) < 5):
        a = _get_recommendation(pick, against, ban)
        recommendations.append(a)
        ban.append(a)

    return recommendations
