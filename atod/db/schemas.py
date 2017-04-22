''' There are a lot of variables in descriptions of every subject in the
    game, so db schemas are pretty complex to write in static form.
    This file provides interface to all schemas through 
'''

import json
import logging
from sqlalchemy import Integer, String, Float

from atod import settings
from atod.db import Base, engine
from atod.preprocessing.dictionary import get_types

logging.basicConfig(level=logging.INFO)

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


class Schema():
    ''' Attempt to create abstraction on all the schemas. unsuccessful.
    
        I'm gonna return to create updating functionality.
    '''
    tables_base_names = ['abilities', 'abilities_specs', 'heroes']

    # get the latest version from engine.tables_names()

    # __tables__ = [('abilities', AbilityModel),
    #               ('abilities_specs', AbilitySpecsModel),
    #               ('heroes', HeroModel)]

    def __init__(self):
        self.current_version = sorted(self._versions)[-1]

    @property
    def _versions(self):
        ''' Set of all prefixes for the tables. '''
        return {v.split('_')[0] for v in Base.metadata.tables.keys()}


    def create_tables(self, version):
        ''' Creates __tables__ with current_version as prefix. '''

        # check if version already exists
        if version in self._versions:
            raise KeyError('Tables for version {}'.format(version)
                           + 'already exist.')
        else:
            self.current_version = version

        for table_name, model in self.__tables__:
            full_name = self.current_version + table_name

            if not engine.has_table(full_name):
                model.__table__.create(bind=engine)
                logging.info(full_name + ' was created.')

    def get_table_name(self, model):
        for name, model_ in  self.__tables__:
            if model_ is model:
                return self.current_version + '_' + name

        raise ValueError('No table for this model -- check __tables__.')


def get_hero_schema():
    return heroes_scheme


def get_ability_specs_schema():
    ''' Creates schema of abilities table.
    
        Raises:
            ValueError: if key contain 2 or more different types and
                they are not float and int.
    
        Returns:
            scheme (dict): keys - all properties in cleaned abilities,
                items - python
    '''

    with open(settings.ABILITIES_LISTS_FILE) as fp:
        skills = json.load(fp)

    keys_types = dict()
    for skill, description in skills.items():
        keys_types[skill] = get_types(description)

    key2type = dict()
    for skill, description in keys_types.items():
        for key, types in description.items():
            key2type.setdefault(key, set())
            key2type[key] = key2type[key].union(types)

    # if key contains both float and ints set types as float
    for key, types in key2type.items():
        # this is not the best way to check types, but for abilities
        # it's ok
        if int in types and float in types:
            key2type[key] = [float]

    for key, types in key2type.items():
        if len(types) > 1:
            raise ValueError('Single key maps to more than one type.')

    scheme = dict()
    for key, types in key2type.items():
        scheme[key] = settings.field_format[types.pop()]

    scheme['name'] = settings.field_format[str]
    scheme['HeroID'] = settings.field_format[int]
    scheme['lvl'] = settings.field_format[int]

    return scheme


def get_item_schema():
    with open(settings.DATA_FOLDER + 'items_types.json', 'r') as fp:
        items_types = json.load(fp)

    items_scheme = {}
    for key, value in items_types.items():
        items_scheme[key] = settings.field_format[value]

    items_scheme['name'] = String
    items_scheme['in_game_name'] = String
    items_scheme['aliases'] = String

    return items_scheme


def get_ability_schema():
    return settings.LABELS