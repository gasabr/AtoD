import os

from atod import settings
from atod.db import session
from atod.db_models.patch import PatchModel


class Meta(object):
    ''' Class stores meta information about versions. '''

    base_files = ['npc_abilities.txt', 'npc_heroes.txt', 'npc_units.txt']

    def __init__(self):
        ''' Finds the last created version and set up lib to use it. '''
        print('init')
        query = session.query(
                    PatchModel.name).order_by(
                    PatchModel.created).limit(1)

        self.name = query.first()[0]
        self.folder = os.path.join(settings.DATA_FOLDER, self.name)

    def add_version(self, name: str, folder: str):
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
        '''

        # check name for uniqueness
        self.name = name

        if os.path.exists(folder):
            self.folder = folder
        else:
            raise FileNotFoundError('folder does not exists')

    def get_tables_prefix(self):
        ''' Returns:
                str: prefix for all the tables of current version, ends with '_'
        '''
        return self.name + '_'


meta_info = Meta()
