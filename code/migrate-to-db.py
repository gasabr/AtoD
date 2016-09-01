#!/usr/bin/env python3

import MySQLdb
import json

import config
import match

# heroes with features to db
def dump_heroes_to_db():
    # get features from old file
    with open('../data/heroes-features.json') as fp:
    heroes = json.load(fp)

	# establish connection
	conn = MySQLdb.connect(host='localhost', db='AtoData' ,user='gasabr', passwd='dotadata')
	dc = conn.cursor()
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

# ti lan matches to db
def fill_matches():
    with open('../data/ti-lan.json') as fp:
        ti_lan = json.load(fp)

    for match_id in ti_lan['matches_ids']:
        tmp_match = config.api.get_match_details(match_id)
        unix_time = tmp_match['start_time']
        result = 1 if tmp_match['radiant_win'] else 0

        radiant_id = tmp_match['radiant_team_id']
        dire_id = tmp_match['dire_team_id']

        conn = MySQLdb.connect(host='localhost', db='AtoData',
                               user='gasabr', passwd='dotadata')
        c = conn.cursor()

        query = """INSERT INTO Matches(id, result, league_id, radiant_id, dire_id, unix_time)
            VALUES(%s, %s, %s, %s, %s, %s)""" % \
                (match_id, result, 4664, radiant_id, dire_id, unix_time)
        # print(query)
        c.execute(query)
        conn.commit()

        c.close()
        conn.close()
