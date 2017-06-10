
# coding: utf-8

# ## IDEA
# Would be nice to find how good one hero works in combination with another. I thought it is possible to count such metric by doing the following:
# 1. Get matches ids (for a patch, a year or any period)
# 2. For all the ids create 2 vectors, representing a team (with help of Match class). Vector contain ids and result.
# 3. Create an adjacency matrix C of the size (n_heroes X n_heroes)
# 4. Go through all the vectors creted on the step 2 and
#     - add some small weight to the C\[i\][j] where i and j are heroes ids if the combination won. Do so for all posible combinations
#     - subtract the same small weight if a team lost

# In[1]:

import json

from atod import Match


# In[2]:

# I extracted picks and result from huge dumb of matches
with open('/Users/gasabr/AtoD/atod/data/picks.json', 'r') as fp:
    matches = json.load(fp)
    
print(len(matches))


# In[3]:

n_heroes = 115
C = [[0 for x in range(n_heroes)] for y in range(n_heroes)]
# the "small wright" what would be added and subtracted
w = 1 / len(matches)
# print(C[1][1])


# In[4]:

def add_weight(C, heroes, w):
    if len(set(heroes)) != 5:
        print('Where is same hero id in one pick')

    for i, hero1 in enumerate(heroes):
        for hero2 in heroes[i+1:]:
            C[hero1][hero2] += w
            C[hero2][hero1] += w

# In[5]:

done = False
for match_id, match in matches.items():
    if not isinstance(match, dict):
        continue
    # get winner side id. Radiant is 0, Dire is 1
    winner = 0 if match['radiant_win'] else 1
    # add w to all the pairs of winner heroes
    add_weight(C, match[str(winner)], w)

    # if C[1][1] != 0 and not done:
    #     # print(match_id)
    #     done = True

    # subtract from all the loser pairs w
    add_weight(C, match[str(abs(winner-1))], -w)

    # if C[1][1] != 0 and not done:
    #     # print(match_id)
    #     done = True
#

# In[ ]:

print(C[19].index(max(C[19])))

# In[ ]:



