#!/usr/bin/env python3

import MySQLdb
import json

import config
import match

first_lan_match_time = 1470156016

# heroes with features to db
def fill_heroes():
    # get features from old file
    with open('../data/heroes-features.json') as fp:
        heroes = json.load(fp)
    # establish connection
    conn = MySQLdb.connect(host='localhost', db='AtoData',
        user='gasabr', passwd='dotadata')
    c = conn.cursor()
    # insert heroes to db
    for hero_id, f in heroes.items():
        query = """INSERT INTO Heroes(name, id, carry, support, nuker, disabler,
            jungler, durable, escape, pusher, initiator)
            VALUES("%s", %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""" % \
            (str(f['name']), int(hero_id), f['carry'], f['support'], f['nuker'], 
            f['disabler'], f['jungler'],f['durable'], f['escape'], f['pusher'],
            f['initiator'])
        c.execute(query)
        conn.commit()
    # close connection
    c.close()
    conn.close()

# ti matches to db
def fill_matches():
    with open('../data/The International 2016.json') as fp:
        ti_lan = json.load(fp)

    conn = MySQLdb.connect(host='localhost', db='AtoData',
        user='gasabr', passwd='dotadata')
    c = conn.cursor()

    for match_id in ti_lan['matches_ids']:
        try:
            match = config.api.get_match_details(match_id)
            unix_time = match['start_time']
            result = 1 if match['radiant_win'] else 0

            radiant_id = match['radiant_team_id']
            dire_id = match['dire_team_id']
        except KeyError as  e:
            print('Match %d cannot be inserted.' % match_id)
        else:
            query = """INSERT INTO Matches(id, result, league_id, radiant_id, dire_id, unix_time)
                VALUES(%s, %s, %s, %s, %s, %s)""" % \
                    (match_id, result, 4664, radiant_id, dire_id, unix_time)
            c.execute(query)
            conn.commit()

    c.close()
    conn.close()

def fill_players():
    conn = MySQLdb.connect(host='localhost', db='AtoData',
        user='gasabr', passwd='dotadata')
    c = conn.cursor()

    teams = {}
    with open('../data/tmp_data.json') as fp:
        teams = json.load(fp)

    for team_name, players in teams.items():
        position = 1
        for player in players:
            query = """INSERT INTO Players(nick, account_id, team, position)
                VALUES('%s', %s, '%s', %s)""" % (player['nick'], player['account_id'],
                team_name, position)
            # print(query)
            c.execute(query)
            conn.commit()

            position += 1

    c.close()
    conn.close()

def fill_teams():
    # NOTE: some names changes in Teams table manually!
    conn = MySQLdb.connect(host='localhost', db='AtoData',
            user='gasabr', passwd='dotadata')
    c = conn.cursor()

    c.execute("SELECT id FROM Matches WHERE unix_time>=%s" % (first_lan_match_time))
    r = c.fetchall()

    teams_set = set()
    match_n = 0
    while len(teams_set) < 18:
        tmp_id = r[match_n][0]
        m = match.Match(tmp_id)
        radiant, dire = m.get_teams()
        teams_set.add(radiant)
        teams_set.add(dire)
        match_n += 1

    # print(teams_set)
    for team in teams_set:

        query = "INSERT INTO Teams(id, name) VALUES(%s, '%s') " % (team[0], team[1])
        print(query)
        c.execute(query)
    conn.commit()
    c.close()
    conn.close()