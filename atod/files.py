''' This module provides interface to program files.

    There can be a few folders with source files, so file paths should be 
    created at the run-time, this module implements idea.
'''

import os

from atod import settings

def get_version_folder():
    ''' Returns path to the current version source folder. '''
    return os.path.join(settings.DATA_FOLDER, settings.CURRENT_VERSION + '/')


def get_heroes_file():
    ''' Returns full path to npc_heroes.txt for current version. '''
    return os.path.join(get_version_folder(), 'npc_heroes.txt')


def get_abilities_specs_schema_file():
    ''' Returns json with abilities_specs schema. '''
    return os.path.join(get_version_folder(), 'abilities_specs_schema.json')


def get_abilities_file():
    ''' Returns full path to npc_heroes.txt for current version. '''
    # current version folder
    return os.path.join(get_version_folder(), 'npc_abilities.txt')


def get_labeled_abilities_file():
    ''' Returns full path to file for current version. '''
    return os.path.join(get_version_folder(), 'labeled_abilities.json')


def get_converter_file():
    return os.path.join(get_version_folder(), 'in_game_converter.json')


def get_schemas_file():
    ''' Returns full path to items.txt for current version. '''
    return os.path.join(get_version_folder(), 'db_schemas.json')


def get_abilities_texts_file():
    ''' Returns path to dota_english.txt file for current version. '''
    return os.path.join(get_version_folder(), 'dota_english.txt')


def get_shops_file():
    ''' Returns path to dota_english.txt file for current version. '''
    return os.path.join(get_version_folder(), 'shops.txt')