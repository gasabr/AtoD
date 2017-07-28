
# coding: utf-8

# In[1]:

import json
import numpy as np
import pandas as pd
from itertools import combinations, product

from atod import Hero, Heroes


# In[2]:

n_heroes = 115


# In[3]:

with open('data/players_in_matches.json', 'r') as fp:
    players_in_matches = json.load(fp)


# In[4]:

# TODO:
# Print some info about dataset:
#  * first match date
#  * last match date
#  * number of matches


# In[5]:

# TODO:
# def how_many_nans(X: pd.DataFrame) -> int:


# In[6]:

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


# In[7]:

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


# In[8]:

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


# In[9]:

# find maximum amount of matches played by 2 heroes
max_matches_played = np.nanmax([np.nanmax(hero) 
                                for hero in matches_together])

# some combinations were played more than another, so
# there is more confidence in picking this kind of heroes (tiny-wi)


# In[10]:

winrate_ = (matches_won / matches_together) * (1 + matches_together / max_matches_played)
winrate = pd.DataFrame(winrate_)
winrate.dropna(axis=0, how='all', inplace=True)
winrate.dropna(axis=1, how='all', inplace=True)
winrate.head()


# In[11]:

lose_rate_ = matches_lost / matches_against
lose_rate = pd.DataFrame(lose_rate_)
lose_rate.dropna(axis=0, how='all', inplace=True)
lose_rate.dropna(axis=1, how='all', inplace=True)
lose_rate.head()


# In[12]:

n = winrate.shape[0]
# how many heroes pairs don't have enough matches to have
# meaningful winrate
n_bad_pairs = n**2 - winrate.count().sum() - (n**2 - n)/2
n_pairs = (n**2 - n)/2
print('Percent of pairs with not enough matches to count them:', 
      n_bad_pairs / n_pairs)


# ## Building a pick
# Idea: user gives 2 heroes as input, after that algorithms searches for the best next hero till there are 5 of them. The best hero would be choosen by maximazing the weight of edges in heroes graph. Heroes graph -- vertices are rows in winrate matrix and edges are winrates of heroes pairs.

# In[13]:

def get_next_hero(pick, against=[], ban=[]):
    best_connection = -100
    next_pick = 0

    for next_hero_id in winrate.index:
        # if this hero is not in the opening
        if next_hero_id not in pick and next_hero_id not in ban                 and next_hero_id not in against:
                
            total_connection = 0
            for picked_hero in pick:
                hero1, hero2 = sorted([next_hero_id, picked_hero])
                total_connection += winrate.loc[hero1][hero2]
                
            for enemy in against:
                total_connection -= lose_rate.loc[next_hero_id][enemy]

            if total_connection > best_connection:
                best_hero = next_hero_id
                best_connection = total_connection

    return best_hero.item()


# In[25]:

pick = Heroes()
pick.add(Hero.from_name(''))

ban = Heroes()
ban.add(Hero.from_name('Shadow Fiend'))
ban.add(Hero.from_name('Invoker'))

against = Heroes()
against.add(Hero.from_name('Slardar'))
against.add(Hero.from_name('Witch Doctor'))

while len(pick) < 5:
    next_hero = get_next_hero(list(pick.get_ids()),
                              ban=list(ban.get_ids()),
                              against=list(against.get_ids()))
    pick.add(Hero(next_hero))
    
print(pick.get_names())


# A lot of attempts to build a pick from a random hero gave me the next thought: maximum weighted winrate should be limited by some value. Because otherwise, same combinations of heroes will appear over and over again. For example, all the values in `winrate` matrix more than .6 should be equal to .6 or weights should be somehow.
# First idea really improves performance!

# In[15]:

h1 = Hero(4)
h2 = Hero(108)
print(h1.name, h2.name)


# In[ ]:



