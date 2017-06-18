''' Provides function for manually updating database. '''
from os import path

from atod import settings
from atod.db import content
from atod.db.create_tables import create_tables


def add_version(folder: str):
    ''' Cretes all needed tables for certain version of the game.

    Args:
        folder: subfolder of settings.DATA_FOLDER, where all files are.

    Raises:

    '''

    # check if provided directory exists
    if not path.exists(folder):
        print('The provided folder {} does not exists.'.format(folder))

    # check if all the needed files exist
    config_files = settings.config_files
    for file_ in config_files:
        full_path = path.join(folder, file_)

        if not path.exists(full_path):
            print('Please, add {} to your version folder.'.format(file_))

    # TODO: check version name for uniquness

    # create tables
    create_tables()

    # fill tables
    content.fill_heroes()
    content.fill_abilities()
    content.fill_abilities_specs()
    content.fill_abilities_texts()
