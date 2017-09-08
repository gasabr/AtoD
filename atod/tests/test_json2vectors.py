import unittest
from os import path

from atod import files

EXAMPLES_FOLDER = path.join(files.TESTS_DATA_FOLDER, 'json2vectors/')


class TestJson2Vectors(unittest.TestCase):

    def test_numeric_part_creation(self):
        pass

if __name__ == '__main__':
    unittest.main()
