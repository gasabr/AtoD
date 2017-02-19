import json
from os import path
from sqlalchemy import Float, Integer, String

CURRENT_VERSION = '702'

HEROES_TABLE_URL = 'http://dota2.gamepedia.com/Table_of_hero_attributes'

#===============================================================================
# Folders, files, paths
#===============================================================================
BASE_FOLDER = path.dirname(path.dirname(path.abspath(__file__)))
DATA_FOLDER = path.join(BASE_FOLDER, 'data/')

NPC_PATH = '/Users/gasabr/Library/Application Support/Steam/steamapps/common/dota 2 beta/game/dota/scripts'

# from game files with data
# TODO: organize such path more accurate / change data/ folder structure
HEROES_FILE = path.join(DATA_FOLDER, 'from-game/npc_heroes.json')
ITEMS_FILE  = path.join(DATA_FOLDER, 'from-game/items.json')
ID_TO_NAME  = path.join(DATA_FOLDER, 'heroes-features.json')
CONVERTER   = path.join(DATA_FOLDER, 'converter.json')

#===============================================================================
# DataBase settings
#===============================================================================
DB_NAME = 'AtoD.db'
DB_PATH = path.join(DATA_FOLDER, DB_NAME)

field_format = {
    'FIELD_FLOAT': Float,
    'FIELD_INTEGER': Integer,
    'FIELD_STRING': String, # added to serialize all fields
}

# sheme for heroes_<v> table
heroes_scheme = {
    "AttributeStrengthGain": Float,
    "MovementSpeed": Integer,
    # "Bot": {
    #     "Build": {},
    #     "HeroType": String, # TODO: parse
    #     "SupportsEasyMode": "1",
    #     "LaningInfo": {
    #         "RequiresFarm": Integer,
    #         "RequiresSetup": Integer,
    #         "RequiresBabysit": Integer,
    #         "ProvidesSetup": Integer,
    #         "SoloDesire": Integer,
    #         "SurvivalRating": Integer,
    #         "ProvidesBabysit": Integer
    #     },
    #     "Loadout": {}
    # },
    "AttackRange": Integer,
    "AttackDamageMax": Integer,
    "AttributeBaseAgility": Integer,
    "AttributeAgilityGain": Float,
    "AttributeBaseIntelligence": Integer,
    # "Ability12": "special_bonus_attack_damage_75", # ForeignKey
    # "Ability4": "axe_culling_blade", # FK
    "url": String,
    "ArmorPhysical": Float,
    # "Ability13": "special_bonus_hp_250", # FK
    "AttributePrimary": String, # TODO: enum this or what? - dummy code better
                                  # how to implement that?
    # "Ability16": "special_bonus_armor_15",
    "Team": String, # TODO: enum this or what?
    # "Ability3": "axe_counter_helix",
    "AttackDamageMin": Integer,
    # "Ability14": "special_bonus_hp_regen_25",
    # "Ability17": "special_bonus_unique_axe",
    "AttributeIntelligenceGain": Float,
    # "HeroUnlockOrder": Integer, # what's that
    # "Ability1": "axe_berserkers_call",
    "AttackAnimationPoint": Float,
    # "Ability2": "axe_battle_hunger",
    "Rolelevels": String, # TODO: parse
    "AttributeBaseStrength": Integer,
    "AttackRate": Float,
    "Role": String, # TODO: parse
    # "HeroID": Integer,
    # "Ability10": "special_bonus_strength_6",
    # "Ability11": "special_bonus_mp_regen_3",
    "MovementTurnRate": Float,
    "AttackCapabilities": String, # TODO: parse
    # "Ability15": "special_bonus_movement_speed_35",
    "AttackAcquisitionRange": Integer,
    # "StatusHealthRegen": Float
}

items_types = {}
with open(DATA_FOLDER + 'items_types.json', 'r') as fp:
    items_types = json.load(fp)

items_scheme = {}
for key, value in items_types.items():
    items_scheme[key] = field_format[value]
