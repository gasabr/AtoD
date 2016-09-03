import json

import config
import player

class Team(object):
	"""docstring for Team"""
	def __init__(self, team_dict):
		"""
		Takes dictionary with 'name', 'team_id', 'heroes_id'
		"""
		self.name = team_dict['name']
		self.team_id = team_dict['team_id']
		self.heroes_ids = team_dict['heroes_ids']
		self.players = []
		# create players
		with open(config.features_file, 'r') as json_file:
			features_dict = json.load(json_file)
			for player_dict in team_dict['players']:
				self.players.append(player.Player(player_dict, features_dict))

		# sort players by the position
		with open(config.acc_id_to_role_file, 'r') as fp:
			acc_id_to_role = json.load(fp)
			for pl in self.players:
				pl.set_role(acc_id_to_role)

		self.sort_players_by_role()

	def as_dict(self):
		"""I don't remember why i need this"""
		tmp = {'tag': self.tag, 'name': self.name,
			'players_ids': self.players_ids}
		return tmp

	def show_features(self):
		"""
		Shows every player features
		"""
		for player in self.players:
			player.show_features()

	def sort_players_by_role(self):
		"""
		Sorts self.players by role from 1 to 5
		"""
		for current_role in range(1, 6):
			for i in range(len(self.players)):
				if self.players[i].role == current_role:
					self.players[current_role-1], self.players[i] = self.players[i], self.players[current_role-1]

