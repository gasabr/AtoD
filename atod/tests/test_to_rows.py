import os
import json
import unittest

from atod import settings
from atod.utils.db.to_rows import ability_to_rows

class TestUtilsDB(unittest.TestCase):

    def setUp(self):
        self.data_folder = os.path.join(settings.TESTS_DATA_FOLDER, 'db/')

    def test_abilities_to_rows(self):
        filename = os.path.join(self.data_folder, 'to_rows.json')
        with open(filename, 'r') as fp:
            tests_data = json.load(fp)

        for test in tests_data:
            results = list(ability_to_rows(test['input']))
            for expected, result in zip(test['output'], results):
                self.assertEqual(expected, result)


if __name__ == '__main__':
    unittest.main()
