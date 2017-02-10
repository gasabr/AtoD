from os import path

HEROES_TABLE_URL = 'http://dota2.gamepedia.com/Table_of_hero_attributes'
BASE_FOLDER = path.dirname(path.dirname(path.abspath(__file__)))
DATA_FOLDER = path.join(BASE_FOLDER, 'data/')

primary_attr_to_int = {
    'agility'   : 0,
    'strength'  : 1,
    'intellect:': 2,
}
