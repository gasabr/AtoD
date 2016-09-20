#!/usr/bin/env python3

import MySQLdb
import json
from sklearn.preprocessing import normalize
import matplotlib.pyplot as plt

import config
import match

def create_acc_id_to_role():
    import json

    file_name = config.data_folder + 'tmp_data.json'
    acc_id_to_role = {}
    with open(file_name, 'r') as fp:
        rosters = json.load(fp)
    for team_name, players in rosters.items():
        role = 1
        for player in players:
            if player['account_id'] in acc_id_to_role.keys():
                print(player)
            try:
                acc_id_to_role[player["account_id"]] = role
                role += 1
            except Exception as e:
                print(player)
    with open(config.acc_id_to_role_file, 'w+') as fp:
        json.dump(acc_id_to_role, fp)
 
# NOTE: one match lost:(
def matches_features_to_file():
    # connect to db
    features_dict = {}
    with open('../data/picks-sum-weighted.json', 'r') as fp:
        features_dict = json.load(fp)
    print(len(features_dict))

    conn = MySQLdb.connect(host=config.db_host, db=config.db_name,
            user=config.db_user, passwd=config.db_passwd)
    c = conn.cursor()

    # get all lan matches ids
    c.execute("SELECT id FROM Matches WHERE unix_time>%s" % (config.first_lan_match_time))
    r = c.fetchall()
    c.close()
    conn.close()
    matches_ids = [i[0] for i in r]

    # get teams features and store it in dict by match_id
    try:
        for match_id in matches_ids:
            if str(match_id) in features_dict.keys():
                continue
            m = match.Match(match_id)
            f_tuple = m.get_teams_features()
            features_dict[match_id] = {}
            features_dict[match_id]['radiant'] = f_tuple[0]
            features_dict[match_id]['dire'] = f_tuple[1]
    except Exception as e:
        raise e
    finally:
        # dump all features sums to file
        with open('../data/picks-sum-weighted.json', 'w+') as fp:
            json.dump(features_dict, fp, indent=1)


picks = {}
with open('../data/picks-sum-weighted.json') as fp:
    picks = json.load(fp)

X = []
for match_id, teams in picks.items():
    X.append(teams['radiant'])
    X.append(teams['dire'])

X_norm = normalize(X)
q = [X[0][i] - X[1][i] for i in range(len(X[0]))]
print(sum(q))
v = [X_norm[0][i] - X_norm[1][i] for i in range(len(X_norm[0]))]
print(sum(v))

i = 0
conn = MySQLdb.connect(host=config.db_host, db=config.db_name,
            user=config.db_user, passwd=config.db_passwd)
c = conn.cursor()
for match_id, p in picks.items():
    p['radiant_norm'] = X_norm[i*2]
    p['dire_norm'] = X_norm[i*2+1]
    c.execute("SELECT result FROM Matches WHERE id=%s" % (match_id))
    result = c.fetchone()
    p['result'] = result
    i+=1
c.close()
conn.close()

correct_prediction = 0
for match_id, features in picks.items():
    f1_nd = features['radiant_norm']
    f2_nd = features['dire_norm']
    f1 = []
    f2 = []
    for f in f1_nd:
        f1.append(f)
    for f in f2_nd:
        f2.append(f)

    f = [f1[i] - f2[i] for i in range(len(f1))]
    f_sum = sum(f)
    x_axis = [1,2,3,4,5,6,7,8,9]
    plt.xlabel('some features')
    plt.ylabel('normalized sum')
    plt.plot(x_axis, f1, 'r-', x_axis, f2, 'b-')
    plt.axis([0,10,0,1])
    plt.grid(True)
    # print(f_sum, features['result'])
    if f_sum > 0 and features['result'][0] == 1:
        correct_prediction += 1
    elif f_sum < 0 and features['result'][0] == 0:
        correct_prediction += 1

    #plt.show()
    #input()

print(correct_prediction)
