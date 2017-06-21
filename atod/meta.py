import os

from atod.db import session, create_tables
from atod.db_models.patch import PatchModel

class Meta(object):
    ''' Class stores meta information about versions. '''

    def __init__(self):
        ''' Finds the last created version and set up lib to use it. '''
        create_tables()

        query = session.query(PatchModel.name).order_by(
                    PatchModel.created).first()

        self._patch_name = query[0]

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
