import unittest
from os import path

from atod import settings

EXAMPLES_FOLDER = path.join(settings.TESTS_DATA_FOLDER, 'json2vectors/')


class TestJson2Vectors(unittest.TestCase):

    def test_numeric_part_creation(self):
        pass

if __name__ == '__main__':
    unittest.main()
