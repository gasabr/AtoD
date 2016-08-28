import dota2api
import urllib.request
import bs4
from bs4 import BeautifulSoup
import json

import config
import team

ti_lan_teams_ids = [2586976, 111474, 1836806, 1838315, 39, 36, 2512249, 2581813, 1148284,
	2783913, 2163, 1375614, 4, 350190, 15, 2777247, 2108395, 3]

api = dota2api.Initialise(api_key=config.API_KEY)

class League(object):
	"""Contains general info, lists of team's, matches's ids"""
	def __init__(self, league_id):
		"""
		Takes league_id
		Creates object with name. To get matches etc use other functions.
		"""
		self.league_id = league_id
		self.matches_ids = set()
		self.lan_matches_ids = set()
		self.teams = []
		self.name = ""
		self.lan_matches = 171

		response = config.api.get_league_listing()

		for league in response['leagues']:
			if league['leagueid'] == self.league_id:
				self.name = league['name']

	def get_teams(self):
		"""
		Takes self.
		Adds Team class objects to league.
		"""
		i = 1
		for team_id in ti_lan_teams_ids:
			# get team from list
			team_dict = api.get_team_info_by_team_id(team_id)['teams'][0]

			# check participation
			for k, v in team_dict.items():
				if v == self.league_id:
					self.teams.append(team.Team(team_dict))
			print('number of teams processed:', i)
			i+=1
		print('total number of teams:', len(self.teams))

	def get_matches_ids(self):
		"""
		Takes nothing.
		Appends matches ids to self.matches_id from dotabuff
		"""
		page_template = 'http://www.dotabuff.com/esports/leagues/' + \
			str(self.league_id) + '/matches?page=%s'

		opener = urllib.request.build_opener()
		# dotabuff server need headers or you will get HTTP Error 429
		opener.addheaders = [('User-agent', 'Mozilla/5.0')]

		# dotabuff displays 20 games per page
		pages_num = round(config.league_matches_num / 20 + .5) + 1
		for i in range(1, pages_num):
			url_opener = opener.open(page_template % (i))

			html_bytes = url_opener.read()
			html_str = html_bytes.decode('utf-8')

			soup = BeautifulSoup(html_str, "lxml")
			links = soup.find_all('a')
			
			for link in links:
			# to delete pages numbers from set check if number more than number of pages
			# TODO: find more universal solution
				if link.get_text().isdigit() and int(link.get_text()) > pages_num:
					self.matches_ids.add(int(link.get_text()))

			print('pages checked', i)

	def get_lan_matches_ids(self):
		"""
		won't work after august 2016, depends from month.
		TODO: implement this for any tournament
		"""
		page_template = 'http://www.dotabuff.com/esports/leagues/' + \
			str(self.league_id) + '/matches?date=month&page=%s'

		opener = urllib.request.build_opener()
		# dotabuff server need headers or you will get HTTP Error 429
		opener.addheaders = [('User-agent', 'Mozilla/5.0')]

		# dotabuff displays 20 games per page
		pages_num = round(self.lan_matches / 20 + .5) + 1
		for i in range(1, pages_num):
			url_opener = opener.open(page_template % (i))

			html_bytes = url_opener.read()
			html_str = html_bytes.decode('utf-8')

			soup = BeautifulSoup(html_str, "lxml")
			links = soup.find_all('a')
			
			for link in links:
			# to delete pages numbers from set check if number more than number of pages
			# have to find more universal solution later
				if link.get_text().isdigit() and int(link.get_text()) > pages_num:
					self.lan_matches_ids.add(int(link.get_text()))

			print('pages checked', i)

	def show_league_info(self):
		"""
		Show name, id, amount of teams and games.
		"""
		print(self.name)
		print(self.league_id)
		print('Total amount of teams:', len(self.teams))
		print('Total amount of games:', len(self.matches_ids))

	def dump_to_file(self, file_name):
		"""
		Parameters:
			file_name - str - variable from config, where to store data
		"""
		tmp = {'name': self.name, 'league_id': self.league_id, 
			'matches_ids': list(self.matches_ids), 
			'teams': [team.as_dict() for team in self.teams]}
		with open(file_name, 'w+') as fp:
			json.dump(tmp, fp, indent=1)

	def get_ti_rosters(self):
		"""
		NOTE: zai's and piliedie's names inserted in file manually.
		Scrap official cite page dump to file teams rosters
		"""
		rosters = {}
		page = 'http://www.dota2.com/international/teams/'

		opener = urllib.request.build_opener()
		opener.addheaders = [('User-agent', 'Mozilla/5.0')]
		html = opener.open(page)

		html_bytes = html.read()

		html_str = html_bytes.decode('utf-8')
		soup = BeautifulSoup(html_str, "lxml")
		divs = soup.find_all('div', class_='Roster')

		for div in divs:
			team_name = div.contents[1][1:-1]
			rosters[team_name] = []
			content = div.contents
			player_dict = {}
			for element in content:
				if isinstance(element, bs4.element.Tag):
					if element.name == 'b':
						player_dict['nick'] = element.contents[0]
						next_index = content.index(element)+1
						name = content[next_index].contents[0]
						name = name.encode('utf-8')
						name = name.decode('unicode_escape')
						player_dict['name'] = name
						rosters[team_name].append(player_dict)
						player_dict = {}				
		with open(config.ti_rosters_file, 'w+') as fp:		
			json.dump(rosters, fp, indent=1)
	
	def get_rosters_ids_manual():
		"""
		Gives opportunity to manually connect player name with account_id,
		will be changed.
		"""
		ti_lan = {}
		with open(config.ti_lan_file, 'r') as fp:
			ti_lan = json.load(fp)

		ti_rosters = {}
		with open(config.ti_rosters_file, 'r') as fp:
			ti_rosters = json.load(fp)

		page_t = 'http://www.dotabuff.com/esports/players/'

		error_count = 1
		not_completed = []

		def get_rosters_ids_manual():
		for team in ti_lan['teams']:
			nicks = []
			if team['name'] in ti_rosters.keys():
				team_index = team['name']
				for player in ti_rosters[team['name']]:
					nicks.append(player['nick'])
			elif team['tag'] in ti_rosters.keys():
				team_index = team['tag']
				for player in ti_rosters[team['tag']]:
					nicks.append(player['nick'])
			else:
				# NOTE: names in opened files are changed!
				print('ERROR: Bad name')
				bad_names.append(team['name'])

			for i in range(1, len(nicks)+1):
				print("{}. {}".format(i, nicks[i-1]))
			for account_id in team['players_ids']:
				try:
					opener = urllib.request.build_opener()
					opener.addheaders = [('User-agent', 'Mozilla/5.0')]
					html = opener.open(page_t + str(account_id))
					html_bytes = html.read()
					html_str = html_bytes.decode('utf-8')
					soup = BS(html_str, 'lxml')
					title_tag = soup.find('title')
					print(title_tag.contents)
					c = input('choose player: ')
					if c != 0:
						ti_rosters[team_index][int(c)-1]['account_id'] = account_id
					else:
						not_completed.append(account_id)
				except Exception as e:
					print(e)
					print('Не получилось,', error_count)
					error_count +=1
				
		print(json.dumps(ti_rosters, indent=1))

		tmp_file_name = config.data_folder + 'tmp_data.json'
		with open(tmp_file_name, 'r') as fp:
			ti_rosters = json.load(fp)

		uncompleted = []
		for team_name, players in ti_rosters.items():
			for player in players:
				if not 'account_id' in player.keys():
					uncompleted.append(player['nick'])
		print(uncompleted)
				