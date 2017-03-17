import os
import json
import unittest

from atod import settings
from atod.tools.cleaning.abilities import min_max2avg

class TestCleaningAbilities(unittest.TestCase):

    def setUp(self):
        self.data_folder = os.path.join(settings.TESTS_DATA_FOLDER,
                                        'cleaning/')

    def test_min_max2avg(self):
        file = os.path.join(self.data_folder, 'min_max2avg.json')
        with open(file, 'r') as fp:
            test_data = json.load(fp)

        for inp, out in zip(test_data['input'], test_data['output']):
            self.assertEqual(min_max2avg(inp), out)


if __name__ == '__main__':
    unittest.main()
