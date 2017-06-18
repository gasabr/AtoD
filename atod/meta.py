import os


class Meta(object):
    ''' Class stores meta information about versions. '''

    base_files = ['npc_abilities.txt', 'npc_heroes.txt', 'npc_units.txt']

    def __init__(self):
        ''' Finds the last created version and set up lib to use it. '''
        pass

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

        self.name = name
        if os.path.exists(folder):
            self.folder = folder
        else:
            raise FileNotFoundError('folder does not exists')

    def get_table_name(table: str):
        ''' Composes the name for the `table` from version and table base name.


        '''
        pass


m = Meta('788', 'some folder')
