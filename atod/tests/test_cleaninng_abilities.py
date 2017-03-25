import os
import json
import unittest

from atod import settings
from atod.tools.cleaning.abilities import (min_max2avg, remove_word,
                                           merge_similar_)

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

    def test_tooltip_removing(self):
        file = os.path.join(self.data_folder, 'tooltip.json')
        with open(file, 'r') as fp:
            test_data = json.load(fp)

        for inp, out in zip(test_data['input'], test_data['output']):
            self.assertEqual(remove_word(inp, word='tooltip'), out)

    def test_similar_merging(self):
        file = os.path.join(self.data_folder, 'merge_similar.json')
        with open(file, 'r') as fp:
            test_data = json.load(fp)

        with open(settings.ABILITIES_CHANGES_FILE, 'r') as fp:
            changes = json.load(fp)

        for case in test_data:
            self.assertEqual(merge_similar_(case['input'], changes),
                             case['output'])


if __name__ == '__main__':
    unittest.main()
