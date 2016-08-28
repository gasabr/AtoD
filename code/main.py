#!/usr/bin/env python3

import dota2api
import json
from pprint import pprint

import config
import pick

api = dota2api.Initialise(api_key='65DCCD4C2595F8E7955797033914EE6B')

# two dictionaries to get name from id and other way
name_to_id = {}
id_to_name = {}
raw_heroes = api.get_heroes()

for hero in raw_heroes['heroes']:
	name_to_id[hero['localized_name']] = hero['id']
	id_to_name[hero['id']] = hero['localized_name']

heroes = {}

with open(config.features_file, 'r') as fp:
	heroes = json.load(fp)

dc = ['Mirana', 'Naga Siren', 'Oracle', 'Tidehunter', 'Razor']
eg = ['Shadow Demon', 'Faceless Void', 'Kunkka', 'Luna', 'Queen of Pain']

dc_pick = pick.Pick(*dc)
eg_pick = pick.Pick(*eg)

dc_pick.get_features_sum()
dc_pick.show_features()

eg_pick.get_features_sum()
eg_pick.show_features()

def _str_to_id():
	pass

def get_features(heroes_list):
	if len(heroes_list) == 0:
		print('List is empty.')
		return 1
	for hero in heroes_list:
		hero_features = get_hero_features()
