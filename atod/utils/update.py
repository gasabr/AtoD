''' Provides function for manually updating database. '''
import os

from sqlalchemy.orm import sessionmaker, scoped_session

from atod.meta import meta_info
from atod.db import content, engine
from atod.db_models import PatchModel
from atod.db_models.ability import AbilityModel
from atod.db_models.ability_specs import AbilitySpecsModel
from atod.db_models.ability_texts import AbilityTextsModel
from atod.db_models.hero import HeroModel

session = scoped_session(sessionmaker(bind=engine))

# files needed to create new version
_game_files = ['npc_abilities.txt', 'npc_heroes.txt', 'dota_english.txt']
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
        meta_info.set_patch(name)

    # fill tables
    content.add_heroes(npc_heroes=os.path.join(folder, 'npc_heroes.txt'),
                       patch=name)
    content.add_abilities(os.path.join(folder, 'labeled_abilities.json'),
                          patch=name)
    content.add_abilities_specs(os.path.join(folder, 'npc_abilities.txt'),
                                patch=name)
    content.add_abilities_texts(os.path.join(folder, 'dota_english.txt'),
                                patch=name)


def delete_patch(name: str):
    ''' Deletes all the records in all tables marked with this patch. 
    
    Args:
        name: patch name

    Raises:
        ValueError: if patch with `name` does not exists.
    '''

    # check if patch with such name exists
    patch = session.query(PatchModel).filter_by(name=name).first()
    if patch is None:
        raise ValueError('Patch with the name {} does not exists'.format(name))

    # remove all the records in all tables
    AbilityModel.delete(patch=name)
    AbilitySpecsModel.delete(patch=name)
    AbilityTextsModel.delete(patch=name)
    HeroModel.delete(patch=name)

    # finally delete patch model
    PatchModel.delete(name=name)

