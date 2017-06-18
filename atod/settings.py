from os import path

# add function which will search for data versions
CURRENT_VERSION = '706'

# ============================================================================
# Folders, files, paths
# ============================================================================
BASE_FOLDER = path.dirname(path.abspath(__file__))
DATA_FOLDER = path.join(BASE_FOLDER, 'data/')
TESTS_DATA_FOLDER = path.join(BASE_FOLDER, 'tests/tests_data/')

NPC_PATH = '/Users/gasabr/Library/Application Support/Steam/steamapps/common/dota 2 beta/game/dota/scripts'

# from game files with data
ABILITIES_CHANGES_FILE  = path.join(DATA_FOLDER, 'abilities_changes.json')

# ============================================================================
# DataBase settings
# ============================================================================
DB_NAME = 'AtoD.db'
DB_PATH = path.join(DATA_FOLDER, DB_NAME)

# tables names
HEROES_TABLE = CURRENT_VERSION + '_heroes'
ITEMS_TABLE = CURRENT_VERSION + '_items'
ABILITIES_SPECS_TABLE = CURRENT_VERSION + '_abilities_specs'
ABILITIES_TEXTS_TABLE = CURRENT_VERSION + '_abilities_texts'
ABILITIES_TABLE = CURRENT_VERSION + '_abilities'

tables = [HEROES_TABLE, ITEMS_TABLE, ABILITIES_SPECS_TABLE]

config_files = ['db_schemas.json', 'in_game_converter.json',
                'labeled_abilities.json']
