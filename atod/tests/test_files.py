import os
import unittest

from atod import files as atod_files


class TestSettings(unittest.TestCase):
    ''' Class to test atod.files.py files

    Checks existance of all the needed files.
    '''
    def test_existance(self):
        ''' Tests existance of files mentioned in settings.

        Files names variables have caps-locked names.
        '''
        settings_dir = dir(atod_files)

        paths_names = ['FOLDER', 'PATH', 'FILE']

        files = [d for d in settings_dir if
                            any(map(lambda x: x in d, paths_names))]

        for var in files:
            # get paths from module
            full_path = getattr(atod_files, var) 
            # test if the paths exists
            self.assertEqual(os.path.exists(full_path), True)


if __name__ == '__main__':
    unittest.main()
