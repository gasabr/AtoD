import os

from atod import settings
from atod.db import session
from atod.db_models.patch import PatchModel
# from atod.db_models.hero import HeroModel
# from atod.db_models.ability import AbilityModel
# from atod.db_models.ability_specs import AbilitySpecsModel
# from atod.db_models.ability_texts import AbilityTextsModel


class Meta(object):
    ''' Class stores meta information about versions. '''

    # files needed to create new version
    game_files = ['npc_abilities.txt', 'npc_heroes.txt', 'npc_units.txt',
                  'dota_english.txt']
    config_files = ['db_schemas.json', 'in_game_converter.json',
                    'labeled_abilities.json']
    # tables = [AbilitySpecsModel, AbilityTextsModel, AbilityModel, HeroModel]

    def __init__(self):
        ''' Finds the last created version and set up lib to use it. '''
        query = session.query(
                    PatchModel.name).order_by(
                    PatchModel.created).limit(1)

        self._patch_name = query.first()[0]
        self._patch_folder = os.path.join(settings.DATA_FOLDER,
                                          self._patch_name)

    def get_tables_prefix(self):
        ''' Returns:
                str: prefix for all the tables ends with '_'.
        '''
        return self._patch_name + '_'

    def get_full_path(self, filename: str):
        ''' Compose full path for source file for current version. 
        
        Args:
            filename: one of the game files or config files.
            
        Returns:
            str: full path for source file.
            
        '''
        return os.path.join(self._patch_folder, filename)

    @property
    def files_list(self):
        files_list = self.game_files + self.config_files
        return files_list

    @property
    def patch(self):
        return self._patch_name

    def set_patch(self, name: str):
        # check if the patch is created in the db
        patches = [p[0] for p in session.query(PatchModel.name).all()]

        if name not in patches:
            raise ValueError('Please, create a record in `patches` table'
                             'before using the patch.')

        self._patch_name = name

meta_info = Meta()
