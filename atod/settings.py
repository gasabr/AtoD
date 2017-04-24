from os import path

# add function which will search for data versions
CURRENT_VERSION = '702'

# ============================================================================
# Folders, files, paths
# ============================================================================
BASE_FOLDER = path.dirname(path.abspath(__file__))
DATA_FOLDER = path.join(BASE_FOLDER, 'data/')
TESTS_DATA_FOLDER = path.join(BASE_FOLDER, 'tests/tests_data/')

NPC_PATH = '/Users/gasabr/Library/Application Support/Steam/steamapps/common/dota 2 beta/game/dota/scripts'

# from game files with data
# TODO: organize such path more  accurate / change data/ folder structure
# HEROES_FILE = path.join(DATA_FOLDER, 'parsed/npc_heroes.json')
# ITEMS_FILE = path.join(DATA_FOLDER, 'parsed/items.json')
# ABILITIES_FILE = path.join(DATA_FOLDER, 'parsed/npc_abilities.json')

# TODO: make one beautiful converter from it (or maybe 2)
# TODO: rename this with FILE
# ID_TO_NAME = path.join(DATA_FOLDER, 'heroes-features.json')
# CONVERTER = path.join(DATA_FOLDER, 'converter.json')
# IN_GAME_CONVERTER = path.join(DATA_FOLDER, 'in_game_converter.json')
#
# DICTIONARY_FOLDER = path.join(DATA_FOLDER, 'dictionary/')
# ABILITIES_DICT_FILE = path.join(DICTIONARY_FOLDER, 'abilities.dict')
# ABILITIES_CORPUS_FILE = path.join(DICTIONARY_FOLDER, 'abilities.mm')
#
# TMP_FOLDER = path.join(DATA_FOLDER, 'tmp/')
# ABILITIES_LABELING_FILE = path.join(TMP_FOLDER, 'abilities_labeling.json')
# ABILITIES_LABELED_FILE  = path.join(TMP_FOLDER, 'abilities_labeled.json')
# ABILITIES_TRAIN_FILE    = path.join(TMP_FOLDER, 'abilities_labeled.json')
ABILITIES_CHANGES_FILE  = path.join(DATA_FOLDER, 'abilities_changes.json')
# CLEAN_ABILITIES_FILE    = path.join(TMP_FOLDER, 'abilities_mean.json')
# TMP_ABILITIES = path.join(DATA_FOLDER, 'tmp_abilities.json')
# ABILITIES_LISTS_FILE    = path.join(TMP_FOLDER, 'abilities_lists.json')
#
# ABILITIES_LISTS_LABELED_FILE = path.join(TMP_FOLDER, 'labeled_lists.json')
#
# ABILITIES_DESCRIPTIONS_FILE = path.join(DATA_FOLDER,
#                                         'abilities_descriptions.json')

# ============================================================================
# DataBase settings
# ============================================================================
DB_NAME = 'AtoD.db'
DB_PATH = path.join(DATA_FOLDER, DB_NAME)

# tables names
HEROES_TABLE = CURRENT_VERSION + '_heroes'
ITEMS_TABLE = CURRENT_VERSION + '_items'
ABILITIES_SPECS_TABLE = CURRENT_VERSION + '_abilities_specs'
ABILITIES_TABLE = CURRENT_VERSION + '_abilities'

tables = [HEROES_TABLE, ITEMS_TABLE, ABILITIES_SPECS_TABLE]
