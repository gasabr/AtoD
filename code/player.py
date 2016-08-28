import config

# the way how data should be presented in player.features list
features_structure = {'carry': 0, 'support': 1, 'nuker': 2, 'disabler': 3, 
'jungler': 4, 'durable': 5, 'escape': 6, 'pusher': 7,'initiator': 8, 'range': 9}

class Player(object):
	"""docstring for Player"""
	def __init__(self, player_dict, features_dict):
		self.account_id = player_dict['account_id']
		self.hero_id = player_dict['hero_id']
		self.features = [0] * 10
		self.role = int()

		# get features
		heroes_features = features_dict[str(self.hero_id)]
		self.hero_name = heroes_features['name']
		for k, v in features_structure.items():
			self.features[v] = heroes_features[k]

	def show_features(self):
		"""
		prints hero name and list of features
		"""
		print(self.hero_name, self.features)

	def set_role(self, acc_id_to_role):
		"""
		will print account_id if hero there is no such hero in 
		acc_id_to role sictionary
		"""
		try:
			self.role = acc_id_to_role[str(self.account_id)]
		except Exception as e:
			print('Please, check this account_id:', self.account_id)
		