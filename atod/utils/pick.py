# coding: utf-8

import os
import json
import numpy as np
import pandas as pd
from itertools import combinations, product

from atod import Hero, Heroes, settings

# number of heroes in the game
_n_heroes = 115
# minimum number of matches for pair of heroes to be included in dataset
min_matches_played = 10
# all winrates above this will be equal to
max_winrate = .65


def _get_winners_loosers(players_in_matches_file):
    ''' Reformats data about matches to handful format.

    Args:
        players_in_matches_file (str): path to the file

    Returns:
        dict: "match_id" -> {winners: [id1, id2], loosers: [id1, id2]}

    '''

    with open(players_in_matches_file, 'r') as fp:
        players_in_matches = json.load(fp)

    matches = dict()

    for record in players_in_matches:
        # describe matches as heroes who win and those who lose
        matches.setdefault(str(record['match_id']),
                           {
                            'winners': [],
                            'loosers': [],
                           }
                          )

        match_id = str(record['match_id'])
        if record['win']:
            # add hero to winners of this match
            matches[match_id]['winners'].append(record['hero_id'])
        else:
            # add hero to losers
            matches[match_id]['loosers'].append(record['hero_id'])

    # length of matches should be 10 times smaller than length of players...
    # since there are 10 players in each match
    assert len(matches), len(players_in_matches) / 10

    return matches


def _count_win_lose_rates(matches):
    ''' Counts win(lose) rates from given matches dictionary. 
    
    This function counts win, loserates and weights results
    '''
    together_matches = np.zeros((_n_heroes, _n_heroes))
    against_matches = np.zeros((_n_heroes, _n_heroes))
    won_matches = np.zeros((_n_heroes, _n_heroes))
    lost_matches = np.zeros((_n_heroes, _n_heroes))

    for match in matches.values():
        # for winners
        # sorting is needed to have upper traingular matrix
        for hero1, hero2 in combinations(sorted(match['winners']), 2):
            together_matches[hero1][hero2] += 1
            won_matches[hero1][hero2] += 1

        for hero1, hero2 in combinations(sorted(match['loosers']), 2):
            together_matches[hero1][hero2] += 1

        # for all posible pairs of winners and loosers
        for looser, winner in product(match['loosers'], match['winners']):
            # add one to matches they played against each other
            against_matches[looser][winner] += 1
            against_matches[winner][looser] += 1
            lost_matches[looser][winner] += 1

    max_together_matches = max([max(a) for a in together_matches])

    # if combination of 2 heroes were used less than `min_matches` times,
    # don't count their win(lose)rate (it would be NaN in result matrix)
    together_matches[together_matches < min_matches_played] = np.NaN
    together_matches[together_matches > max_winrate] = max_winrate
    against_matches[against_matches < min_matches_played] = np.NaN

    # find maximum amount of matches played by 2 heroes
    max_matches_played = np.nanmax([np.nanmax(hero)
                                    for hero in together_matches])

    # some combinations were played more than another, so
    # there is more confidence in picking this kind of heroes
    winrate_ = (won_matches / together_matches)
    # weigth winrates based on amount of matches played together
    winrate_ *= (1 + together_matches / max_matches_played)
    winrates = pd.DataFrame(winrate_)
    winrates.dropna(axis=0, how='all', inplace=True)
    winrates.dropna(axis=1, how='all', inplace=True)

    loserates_ = lost_matches / against_matches
    loserates = pd.DataFrame(loserates_)
    loserates.dropna(axis=0, how='all', inplace=True)
    loserates.dropna(axis=1, how='all', inplace=True)

    return winrates, loserates

# XXX: strange: to get file and do not use it if .csv already exists
def _get_win_lose_rates(matches_file):
    ''' Returns matrix with win and loserates for all heroes.
    
    Args:
        matches_file (str): file to read matches from 

    Returns:
        (pd.DataFrame, pd.DataFrame): winrates, loserates

    '''

    # TODO: search for files in the same directory with the matches_file
    winrates_file = os.path.join(settings.DATA_FOLDER, 'winrates.csv')
    loserates_file = os.path.join(settings.DATA_FOLDER, 'loserates.csv')

    # try to load files, if unsuccesful - create them from `matches_file`
    try:
        winrates = pd.read_csv(winrates_file, index_col=0)
        loserates = pd.read_csv(loserates_file, index_col=0)

        return winrates, loserates

    except FileNotFoundError:
        matches = _get_winners_loosers(matches_file)

    winrates, loserates = _count_win_lose_rates(matches)

    # write files to ease usage in the next time
    winrates.to_csv(winrates_file)
    loserates.to_csv(loserates_file)

    return winrates, loserates

# TODO: remove global variable (settings.MATCHES_FILE) usage (local is not fix)
# probably, updated Meta would be nice solution
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

    winrates, loserates = _get_win_lose_rates(settings.MATCHES_FILE)

    for next_hero_id in winrates.index.tolist():
        # if this hero is not in the opening
        if next_hero_id not in pick_ids and next_hero_id not in ban_ids \
                and next_hero_id not in against_ids:

            total_connection = 0
            for picked_hero in pick_ids:
                hero1, hero2 = sorted([next_hero_id, picked_hero])
                total_connection += winrates.loc[hero1][hero2]

            for enemy in against_ids:
                total_connection -= loserates.loc[next_hero_id][enemy]

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
