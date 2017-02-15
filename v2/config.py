from os import path

HEROES_TABLE_URL = 'http://dota2.gamepedia.com/Table_of_hero_attributes'
BASE_FOLDER = path.dirname(path.dirname(path.abspath(__file__)))
DATA_FOLDER = path.join(BASE_FOLDER, 'data/')

NPC_PATH = '/Users/gasabr/Library/Application Support/Steam/steamapps/common/dota 2 beta/game/dota/scripts'

DB_NAME = 'AtoD.db'
DB_PATH = path.join(DATA_FOLDER, DB_NAME)

primary_attr_to_int = {
    'agility'   : 0,
    'strength'  : 1,
    'intellect:': 2,
}
