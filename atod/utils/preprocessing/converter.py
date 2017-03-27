#!/usr/bin/env python3
import json
import dota2api
from os import path
from YamJam import yamjam

from atod import settings

api_key = yamjam()['AtoD']['DOTA2_API_KEY']

api = dota2api.Initialise(api_key)

response = api.get_heroes()

in_game_names = {}
for hero in response['heroes']:
    # hero name without npc_dota_hero
    clean_name = hero['name'].split('_hero_')[1]
    in_game_names[clean_name] = hero['id']
    in_game_names[hero['id']] = clean_name

dump_to = path.join(settings.DATA_FOLDER, 'in_game_converter.json')

with open(dump_to, "w+") as fp:
    json.dump(in_game_names, fp, indent=2)
