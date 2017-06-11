import json
import os
import unittest

from atod import settings
from atod.utils.json2rows import ability_to_row


class TestUtilsDB(unittest.TestCase):

    def setUp(self):
        self.data_folder = os.path.join(settings.TESTS_DATA_FOLDER, 'db/')

    def test_abilities_to_rows(self):
        filename = os.path.join(self.data_folder, 'to_rows.json')
        with open(filename, 'r') as fp:
            tests_data = json.load(fp)

        for test in tests_data:
            results = list(ability_to_row(test['input'], test['scheme']))
            for expected, result in zip(test['output'], results):
                self.assertEqual(expected, result)

    # def test_parsing_skills_names(self):
    #     with open(settings.ABILITIES_LISTS_FILE, 'r') as fp:
    #         skills = list(json.load(fp))
    #
    #     # TODO: move this to function
    #     with open(settings.IN_GAME_CONVERTER, 'r') as fp:
    #         converter = json.load(fp)
    #
    #     heroes_names = [c for c in converter.keys()
    #                     if re.findall(r'[a-zA-Z|\_]+', c)]
    #
    #     print(json.dumps())


if __name__ == '__main__':
    unittest.main()
