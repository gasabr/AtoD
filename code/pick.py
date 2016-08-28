import json

class Pick(object):
	"""Contain list of heroes and sum of their features"""
	def __init__(self, *arg):
		"""
		Takes list of id (can be empty)
		"""
		self.heroes = []
		self.features = [0] * len(features_structure)

		if len(arg) != 0:
			for i  in range(len(arg)):
				self.heroes.append(Hero(arg[i]))

	def add_hero(self, hero):
		self.heroes.append(hero)

	def show_heroes(self):
		"""Print names of heroes"""
		for hero in self.heroes:
			print(hero.name, end=", ")

	def get_features_sum(self):
		"""
		Takes name of json file with features
		Writes sum of heroes features to self.features
		Returns nothing
		"""
		# reading from file
		with open(config.features_file, 'r') as json_file:
			features_dict = json.load(json_file)
			for hero in self.heroes:
				hero.get_features(features_dict)

		# summing up
		for hero in self.heroes:
			for i in range(len(features_structure)):
				self.features[i] += hero.features[i]		

	def show_features(self):
		print(self.features)