''' There are a lot of variables in descriptions of every subject in the
    game, so db schemas are pretty complex to write in static form.
    This file provides interface to all schemas through function calls.
'''

import json
import logging

from sqlalchemy import Integer, String, Float

from atod import settings
from atod.utils.dictionary import get_types

logging.basicConfig(level=logging.INFO)


field_format = {
    'FIELD_FLOAT': Float,
    'FIELD_INTEGER': Integer,
    'FIELD_STRING': String,
    int: Integer,
    str: String,
    float: Float
}

type_to_string = {
    int: 'FIELD_INTEGER',
    str: 'FIELD_STRING',
    float: 'FIELD_FLOAT',
    Float: 'FIELD_FLOAT',
    Integer: 'FIELD_INTEGER',
    String: 'FIELD_STRING',
}

LABELS = ['stun', 'transformation', 'slow', 'durability', 'nuke',
          'escape', 'non_hero', 'attack_bonus', 'heal',
          'based_on_attr', 'aoe', 'period_damage', 'attack_debuff',
          'invis', 'vision', 'silence', 'lifesteal', 'armor_buff',
          'armor_debuff', 'save', 'move_speed_buff', 'illusions', 'chance',
          'multiply_heroes', 'global', 'shield', 'attribute_gain',
          'amplify_magic_dmg', 'summon_unit', 'regen', 'daytime_dependent',
          'stacks', 'purge', 'in_percents']

# This dictionary is staying there to remind that not all the information
# about the hero is presented in current schema
heroes_schema = {
    "AttributeStrengthGain": Float,
    "MovementSpeed": Integer,
    # "Bot": {
    #     "Build": {},
    "HeroType": String,
    #     "SupportsEasyMode": "1",
    #     "LaningInfo": {
    "RequiresFarm": Integer,
    "RequiresSetup": Integer,
    "RequiresBabysit": Integer,
    "ProvidesSetup": Integer,
    "SoloDesire": Integer,
    "SurvivalRating": Integer,
    "ProvidesBabysit": Integer,
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
    "AttributePrimary": String,
    # how to implement that?
    # "Ability16": "special_bonus_armor_15",
    "Team": String,
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
    # "HeroID": Integer,
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

''' Description of how get_<table name>_schema functions works and why.

    In the source files FIELD_INTEGER and etc are used, schemas in 
    order to be json serializable are described with the same strings. All
    get_<table name>_schema functions are doing the same job: 
    * open db_schemas file
    * read needed dictionary
    * map strings to SQLAlchemy types
    * return results
'''

''' heroes table'''
def get_heroes_schema():
    ''' Reads heroes schema form db_schemas and returns types mapped to sql.

        Returns:
            heroes_schema (dict): mapping of column name to its SQLAlchemy
                                  type
    '''

    with open(settings.DB_SCHEMAS_FILE, 'r') as fp:
        heroes_schema = json.load(fp)['heroes']

    for column in heroes_schema:
        for key, value in column.items():
            # if value in `field_format` - change value to SQLAlchemy type
            if value in field_format:
                column[key] = field_format[value]

    return heroes_schema


def get_heroes_columns():
    ''' Returns list of columns names for heroes table. '''
    return [column['name'] for column in get_heroes_schema()]


''' abilities_specs table '''
def get_abilities_specs_schema():
    ''' Creates schema of abilities table.
    
        Raises:
            ValueError: if key contain 2 or more different types and
                they are not float and int.
    
        Returns:
            scheme (dict): keys - all properties in cleaned abilities,
                items - python
    '''

    with open(settings.DB_SCHEMAS_FILE, 'r') as schemas_file:
        schema = json.load(schemas_file)['abilities_specs']

    for column in schema:
        for key, value in column.items():
            # if value in `field_format` - change value to SQLAlchemy type
            if value in field_format:
                column[key] = field_format[value]

    return schema


def get_abilities_specs_columns():
    ''' Returns names of columns in abilties_specs table. '''
    return [col['name'] for col in get_abilities_specs_schema()]


def _create_abilities_specs_schema(cleaned_abilities, save_to=None):
    ''' Creates SQLAlchemy schema based on cleaned npc_abilities.txt file.

        "Clean" mean flat, containing only heroes abilities.

        Args:
            cleaned_abilities (dict): cleaned abilities
            save_to (str)           : path to save schema
    '''

    keys_types = dict()
    for skill, description in cleaned_abilities.items():
        keys_types[skill] = get_types(description)

    key2type = dict()
    for skill, description in keys_types.items():
        for key, types in description.items():
            key2type.setdefault(key, set())
            key2type[key] = key2type[key].union(types)

    # if key contains both float and ints set types as float
    for key, types in key2type.items():
        # this is not the best way to check types, but for abilities it's ok
        if int in types and float in types:
            key2type[key] = [float]

    for key, types in key2type.items():
        if len(types) > 1:
            raise ValueError('Single key maps to more than one type.')

    schema = dict()
    for key, types in key2type.items():
        schema[key] = type_to_string[types.pop()]

    schema['name'] = type_to_string[str]
    schema['HeroID'] = type_to_string[int]
    schema['lvl'] = type_to_string[int]

    if save_to is not None:
        with open(save_to, 'w+') as fp:
            json.dump(schema, fp, indent=2)

    return schema


''' abilities table'''
def get_abilities_schema():
    with open(settings.DB_SCHEMAS_FILE, 'r') as schemas_file:
        ability_schema = json.load(schemas_file)['abilities']

    for column in ability_schema:
        for key, value in column.items():
            # if value in `field_format` - change value to SQLAlchemy type
            if value in field_format:
                column[key] = field_format[value]

    return ability_schema
