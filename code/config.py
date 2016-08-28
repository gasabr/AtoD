import dota2api

API_KEY = '65DCCD4C2595F8E7955797033914EE6B'
api = dota2api.Initialise(API_KEY)

data_folder = '../data/'
features_file_xlsx = data_folder + 'dota-data.xlsx'
features_file = data_folder + 'heroes-features.json'
ti_file = data_folder + 'The International 2016' + '.json'
ti_lan_file = data_folder + 'ti-lan.json'
ti_rosters_file = data_folder + 'ti_rosters.json'
acc_id_to_role_file = data_folder + 'acc_id_to_role.json'

league_name = 'The International 2016'
league_id = 4664
league_matches_num = 399