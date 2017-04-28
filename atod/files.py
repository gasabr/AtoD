''' This module provides interface to program files.

    There can be a few folders with source files, so file paths should be 
    created at the run-time, this module implements idea.
'''

import os

from atod import settings


def get_heroes_file():
    ''' Returns full path to npc_heroes.txt for current version. '''

    # current version folder
    version_folder = os.path.join(settings.DATA_FOLDER,
                                  settings.CURRENT_VERSION + '/')

    # folder with raw files
    source_folder = os.path.join(version_folder, 'source/')
    file_path  = os.path.join(source_folder, 'npc_heroes.txt')

    return file_path


def get_abilities_specs_schema_file():
    ''' Returns json with abilities_specs schema. '''
    version_folder = os.path.join(settings.DATA_FOLDER,
                                  settings.CURRENT_VERSION + '/')

    # folder with raw files
    file_path  = os.path.join(version_folder, 'abilities_specs_schema.json')

    return file_path


def get_abilities_file():
    ''' Returns full path to npc_heroes.txt for current version. '''
    # current version folder
    version_folder = os.path.join(settings.DATA_FOLDER,
                                  settings.CURRENT_VERSION + '/')

    # folder with raw files
    source_folder = os.path.join(version_folder, 'source/')
    file_path  = os.path.join(source_folder, 'npc_abilities.txt')

    return file_path


def get_labeled_abilities_file():
    ''' Returns full path to file for current version. '''
    # current version folder
    version_folder = os.path.join(settings.DATA_FOLDER,
                                  settings.CURRENT_VERSION + '/')

    # folder with raw files
    source_folder = os.path.join(version_folder, 'source/')
    file_path  = os.path.join(source_folder, 'labeled_abilities.json')

    return file_path


def get_converter_file():
    # current version folder
    version_folder = os.path.join(settings.DATA_FOLDER,
                                  settings.CURRENT_VERSION + '/')

    file_path  = os.path.join(version_folder, 'in_game_converter.json')

    return file_path


def get_abilities_descriptions_file():
    ''' Returns full path to dota_english.txt for current version. '''
    pass


def get_schemas_file():
    ''' Returns full path to items.txt for current version. '''
    # current version folder
    version_folder = os.path.join(settings.DATA_FOLDER,
                                  settings.CURRENT_VERSION + '/')

    file_path  = os.path.join(version_folder, 'db_schemas.json')

    return file_path