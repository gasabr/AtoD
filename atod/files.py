from os import path



# this is just the way to access secret files in public projects
# fill free to replace the right part with your API key or
# learn how to use YamJam here: http://yamjam.readthedocs.io/en/v0.1.7/
#  DOTA_API_KEY = yamjam()['AtoD']['DOTA2_API_KEY']

# ============================================================================
# Folders, files, paths
# ============================================================================
BASE_FOLDER = path.dirname(path.abspath(__file__))
DATA_FOLDER = path.join(BASE_FOLDER, 'data/')
TESTS_DATA_FOLDER = path.join(BASE_FOLDER, 'tests/tests_data/')

# from game files with data
ABILITIES_CHANGES_FILE  = path.join(DATA_FOLDER, 'abilities_changes.json')
CONVERTER_FILE  = path.join(DATA_FOLDER, 'in_game_converter.json')

# ============================================================================
# DataBase settings
# ============================================================================
DB_NAME = 'AtoD.db'
DB_PATH = path.join(DATA_FOLDER, DB_NAME)
DB_SCHEMAS_FILE = path.join(DATA_FOLDER, 'db_schemas.json')

config_files = ['db_schemas.json', 'in_game_converter.json',
                'labeled_abilities.json']
