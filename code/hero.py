class Hero(object):
	"""Contain name and id, features of hero"""
	def __init__(self, arg):
		if not isinstance(arg, int):
			self.name = arg
			self.hero_id = name_to_id[self.name]
		else:
			self.hero_id = arg
			self.name = id_to_name[arg]
		self.features = [0] * len(features_structure)

	def get_features(self, features_dict):
		"""
		Takes dict of features
		Returns list of features for this hero
		"""
		tmp_features = features_dict[str(self.hero_id)]

		# map features from file with stable structure
		for key, index in features_structure.items():
			self.features[index] = tmp_features[key] 
			
		return self.features