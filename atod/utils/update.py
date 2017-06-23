''' Provides function for manually updating database. '''
import os

from atod.db import content, session
from atod.db_models import PatchModel


# files needed to create new version
_game_files = ['npc_abilities.txt', 'npc_heroes.txt', 'npc_units.txt',
              'dota_english.txt']
_config_files = ['in_game_converter.json', 'labeled_abilities.json']

_version_files = _game_files + _config_files


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

    # fill tables
    content.add_heroes(npc_heroes=os.path.join(folder, 'npc_heroes.txt'),
                        patch=name)
    content.add_abilities(os.path.join(folder, 'labeled_abilities.json'),
                          patch=name)
    content.add_abilities_specs(os.path.join(folder, 'npc_abilities.txt'),
                                patch=name)
    content.add_abilities_texts(os.path.join(folder, 'dota_english.txt'),
                                patch=name)
