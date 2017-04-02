import json
from os import path
from sqlalchemy import Float, Integer, String

CURRENT_VERSION = '702'

HEROES_TABLE_URL = 'http://dota2.gamepedia.com/Table_of_hero_attributes'

# ============================================================================
# Folders, files, paths
# ============================================================================
BASE_FOLDER = path.dirname(path.abspath(__file__))
DATA_FOLDER = path.join(BASE_FOLDER, 'data/')
TESTS_DATA_FOLDER = path.join(BASE_FOLDER, 'tests/tests_data/')

NPC_PATH = '/Users/gasabr/Library/Application Support/Steam/steamapps/common/dota 2 beta/game/dota/scripts'

# from game files with data
# TODO: organize such path more accurate / change data/ folder structure
HEROES_FILE = path.join(DATA_FOLDER, 'parsed/npc_heroes.json')
ITEMS_FILE = path.join(DATA_FOLDER, 'parsed/items.json')
ABILITIES_FILE = path.join(DATA_FOLDER, 'parsed/npc_abilities.json')

# TODO: make one beautiful converter from it (or maybe 2)
# TODO: rename this with FILE
ID_TO_NAME = path.join(DATA_FOLDER, 'heroes-features.json')
CONVERTER = path.join(DATA_FOLDER, 'converter.json')
IN_GAME_CONVERTER = path.join(DATA_FOLDER, 'in_game_converter.json')

DICTIONARY_FOLDER = path.join(DATA_FOLDER, 'dictionary/')
ABILITIES_DICT_FILE = path.join(DICTIONARY_FOLDER, 'abilities.dict')
ABILITIES_CORPUS_FILE = path.join(DICTIONARY_FOLDER, 'abilities.mm')

TMP_FOLDER = path.join(DATA_FOLDER, 'tmp/')
ABILITIES_LABELING_FILE = path.join(TMP_FOLDER, 'abilities_labeling.json')
ABILITIES_LABELED_FILE  = path.join(TMP_FOLDER, 'abilities_labeled.json')
ABILITIES_TRAIN_FILE    = path.join(TMP_FOLDER, 'abilities_labeled.json')
ABILITIES_CHANGES_FILE  = path.join(DATA_FOLDER, 'abilities_changes.json')
CLEAN_ABILITIES_FILE    = path.join(TMP_FOLDER, 'abilities_mean.json')
TMP_ABILITIES = path.join(DATA_FOLDER, 'tmp_abilities.json')
ABILITIES_LISTS_FILE    = path.join(TMP_FOLDER, 'abilities_lists.json')

ABILITIES_LISTS_LABELED_FILE = path.join(TMP_FOLDER, 'labeled_lists.json')

# ============================================================================
# DataBase settings
# ============================================================================
DB_NAME = 'AtoD.db'
DB_PATH = path.join(DATA_FOLDER, DB_NAME)

# tables names
# i cannot understand how to do it generally in SQLAlchemy, so for now
HEROES_TABLE = CURRENT_VERSION + '_heroes'
ITEMS_TABLE = CURRENT_VERSION + '_items'
ABILITIES_SPECS_TABLE = CURRENT_VERSION + '_abilities_specs'
ABILITIES_TABLE = CURRENT_VERSION + '_abilities'

tables = [HEROES_TABLE, ITEMS_TABLE, ABILITIES_SPECS_TABLE]

field_format = {
    'FIELD_FLOAT': Float,
    'FIELD_INTEGER': Integer,
    'FIELD_STRING': String,
    int: Integer,
    str: String,
    float: Float
}

# scheme for heroes_<v> table
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
    # "url": String,
    "ArmorPhysical": Float,
    # "Ability13": "special_bonus_hp_250", # FK
    "AttributePrimary": String,  # TODO: enum this or what? - dummy code better
    # how to implement that?
    # "Ability16": "special_bonus_armor_15",
    "Team": String,  # TODO: enum this or what?
    # "Ability3": "axe_counter_helix",
    "AttackDamageMin": Integer,
    # "Ability14": "special_bonus_hp_regen_25",
    # "Ability17": "special_bonus_unique_axe",
    "AttributeIntelligenceGain": Float,
    # "HeroUnlockOrder": Integer, # what's that
    # "Ability1": "axe_berserkers_call",
    "AttackAnimationPoint": Float,
    # "Ability2": "axe_battle_hunger",
    "Rolelevels": String,  # TODO: parse
    "AttributeBaseStrength": Integer,
    "AttackRate": Float,
    "Role": String,  # TODO: parse
    "HeroID": Integer,
    # "Ability10": "special_bonus_strength_6",
    # "Ability11": "special_bonus_mp_regen_3",
    "MovementTurnRate": Float,
    "AttackCapabilities": String,  # TODO: parse
    # "Ability15": "special_bonus_movement_speed_35",
    "AttackAcquisitionRange": Integer,
    "aliases": String,
    "in_game_name":  String,
    "name": String
    # "StatusHealthRegen": Float
}

with open(DATA_FOLDER + 'items_types.json', 'r') as fp:
    items_types = json.load(fp)

items_scheme = {}
for key, value in items_types.items():
    items_scheme[key] = field_format[value]

items_scheme['name'] = String
items_scheme['in_game_name'] = String
items_scheme['aliases'] = String

LABELS = ['stun', 'transformation', 'slow', 'durability', 'nuke',
          'escape', 'non-hero', 'attack_bonus', 'heal',
          'based on attr', 'aoe', 'period damage', 'attack debuff',
          'invis', 'vision', 'silence', 'lifesteal', 'armor buff',
          'armor debuff', 'save', 'move speed buff', 'illusions', 'chance',
          'multiply heroes', 'global', 'shield', 'attribute gain',
          'amplify magic dmg', 'summon unit', 'regen', 'daytime dependent',
          'stacks', 'purge', 'in percents']