#!/usr/bin/env python3

import dota2api
import json
import urllib.request
from bs4 import BeautifulSoup as BS

import config
import league
import match

file_name = config.data_folder + 'tmp_data.json'
acc_id_to_role = {}
with open(file_name, 'r') as fp:
	rosters = json.load(fp)

def create_acc_id_to_role():
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

create_acc_id_to_role()

with open(config.ti_lan_file, 'r') as fp:
	matches_ids = json.load(fp)['matches_ids']

test_match = match.Match(matches_ids[3])

test_match.compare_features()
