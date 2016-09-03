# only lan matches for ti now

import json

import config
import team 
import pick
import hero

class Match(object):
	"""docstring for Match"""
	def __init__(self, match_id):
		"""
		Takes match_id
		Creates Match object with:
			time - unix stamp
			result - true radiant won
			radiant, dire = Team()
		"""
		self.match_id = match_id
		tmp_match = config.api.get_match_details(self.match_id)
		self.time = tmp_match['start_time']
		self.result = tmp_match['radiant_win']

		# TODO: move this part of code to func
		radiant_dict = {}
		dire_dict = {}
		
		radiant_dict['name'] = tmp_match['radiant_name']
		dire_dict['name'] = tmp_match['dire_name']
		radiant_dict['team_id'] = tmp_match['radiant_team_id']
		dire_dict['team_id'] = tmp_match['dire_team_id']

		radiant_dict['heroes_ids'] = []
		dire_dict['heroes_ids'] = []

		for choise in tmp_match['picks_bans']:
			if choise['is_pick']:
				if choise['team']:
					radiant_dict['heroes_ids'].append(choise['hero_id'])
				else:
					dire_dict['heroes_ids'].append(choise['hero_id'])

		# get connection between player and hero
		players = []
		player_dict = {}	
		# players_tmp = tmp_match.pop('players')
		for player in tmp_match['players']:
			player_dict['account_id'] = player['account_id']
			player_dict['hero_id'] = player['hero_id']
			players.append(player_dict)
			player_dict = {}

		# sort players to team
		radiant_dict['players'] = []
		dire_dict['players'] = []

		for player in players:
			if player['hero_id'] in radiant_dict['heroes_ids']:
				radiant_dict['players'].append(player)
			else:
				dire_dict['players'].append(player)

		self.radiant = team.Team(radiant_dict)
		self.dire = team.Team(dire_dict)

	def compare_features(self):
		"""
		Will show you names of heroes and their features by sides
		"""
		print('Radiant:')
		self.radiant.show_features()
		print('Dire:')
		self.dire.show_features()

	def get_teams(self):
		return(self.radiant.return_info_to_db(), self.dire.return_info_to_db())

		