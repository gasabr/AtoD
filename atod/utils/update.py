''' Provides function for manually updating database. '''
import os

from atod.db import content, session
from atod.db_models import PatchModel
from atod.db.create_tables import create_tables


# files needed to create new version
_game_files = ['npc_abilities.txt', 'npc_heroes.txt', 'npc_units.txt',
              'dota_english.txt']
_config_files = ['db_schemas.json', 'in_game_converter.json',
                'labeled_abilities.json']

_version_files = _game_files + _config_files


def add_version_(self, name: str, folder: str):
    ''' Adds new version from the files in `folder`.

    Notes:
        `name` will be used as prefix for all the tables for this version.
        `name` does not contain points, but can contain a letter, for
        example 687e is correct.

    Args:
        name: the name of the folder in data/ which contain version files.
        folder: path to game/dota/scripts folder.

    Raises:
        FileNotFoundError: if folder does not exists.
        ValueError: if version name is not unique
    '''

    # check name for uniqueness
    versions = [v[0] for v in session.query(PatchModel.name).all()]
    if name in versions:
        raise ValueError('Please pick unique version name.')
    else:
        self.name = name

    if not os.path.exists(folder):
        raise FileNotFoundError('folder does not exists')
    else:
        self.folder = folder


def add_patch(name: str, folder: str):
    ''' Creates all needed tables for certain version of the game.

    Args:
        folder: subfolder of settings.DATA_FOLDER, where all files are.
        name: the name of the folder in data/ which contain version files.

    Raises:
        FileNotFoundError: if folder does not exists.
        ValueError: if version name is not unique.

    '''

    # check if provided directory exists
    if not os.path.exists(folder):
        print('The provided folder {} does not exists.'.format(folder))

    # check if all the needed files exist
    for file_ in _version_files:
        full_path = os.path.join(folder, file_)

        if not os.path.exists(full_path):
            print('Please, add {} to your version folder.'.format(file_))

    versions = [v[0] for v in session.query(PatchModel.name).all()]
    if name in versions:
        raise ValueError('Please pick unique version name.')
    else:
        # change current version in meta
        patch = PatchModel(name)
        session.add(patch)
        session.commit()

    # create tables for the new patch (meta info stores new version)
    create_tables()

    # fill tables
    content.fill_heroes()
    content.fill_abilities()
    content.fill_abilities_specs()
    content.fill_abilities_texts()
