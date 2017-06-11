import json
import os
import unittest

from atod import settings
from atod.utils.abilities import (_average_ability_properties, _remove_word,
                                  _merge_similar)


class TestCleaningAbilities(unittest.TestCase):

    def setUp(self):
        self.data_folder = os.path.join(settings.TESTS_DATA_FOLDER,
                                        'cleaning/')

    def test_average_properties(self):
        file = os.path.join(self.data_folder, 'min_max2avg.json')
        with open(file, 'r') as fp:
            test_data = json.load(fp)

        for case in test_data:
            self.assertEqual(_average_ability_properties(case['input']),
                             case['output'])

    def test_tooltip_removing(self):
        file = os.path.join(self.data_folder, 'tooltip.json')
        with open(file, 'r') as fp:
            test_data = json.load(fp)

        for case in test_data:
            self.assertEqual(_remove_word(case['input'], word='tooltip'),
                             case['output'])

    def test_similar_merging(self):
        file = os.path.join(self.data_folder, 'merge_similar.json')
        with open(file, 'r') as fp:
            test_data = json.load(fp)

        with open(settings.ABILITIES_CHANGES_FILE, 'r') as fp:
            changes = json.load(fp)

        for case in test_data:
            self.assertEqual(_merge_similar(case['input'], changes),
                             case['output'])


if __name__ == '__main__':
    unittest.main()
