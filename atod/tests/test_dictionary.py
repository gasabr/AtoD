import json
import unittest
from os.path import join

from atod import settings
from atod.tools import dictionary

class TestDictionary(unittest.TestCase):
    ''' Tests for functions from dictionary module. '''

    def setUp(self):
        self.data_folder = join(settings.TESTS_DATA_FOLDER, 'dictionary/')

    def test_make_flat_dict(self):
        filename = join(self.data_folder, 'make_flat_dict.json')
        with open(filename, 'r') as fp:
            data = json.load(fp)

        result = dictionary.make_flat_dict(data['input'])

        self.assertEqual(result, data['output'])

    def test_collect_kv(self):
        filename = join(self.data_folder, 'collect_kv.json')
        with open(filename, 'r') as fp:
            data = json.load(fp)

        result = dictionary.collect_kv(data['input'],
                                       exclude=['Version', 'var_type'])

        self.assertEqual(sorted(result, key=lambda k: list(k.keys())[0]),
                 sorted(data['output'], key=lambda k: list(k.keys())[0]))

    # TODO: test with different set of attributes
    def test_all_keys(self):
        filename = join(self.data_folder, 'all_keys.json')
        with open(filename, 'r') as fp:
            data = json.load(fp)

        result = list(dictionary.all_keys(data['input'],
                                          exclude=['Version', 'var_type'],
                                          include_dict_keys=False))

        self.assertEqual(sorted(result), sorted(data['output']))

    def test_extract_effects(self):
        filename = join(self.data_folder, 'extract_effects.json')
        with open(filename, 'r') as fp:
            data = json.load(fp)

        result = dictionary.extract_effects(data['input'])

        self.assertEqual(sorted(result), sorted(data['output']))

    def test_find_all_values(self):
        filename = join(self.data_folder, 'find_all_values.json')
        with open(filename, 'r') as fp:
            data = json.load(fp)

        result = dictionary.find_all_values(data['input'])

        self.assertEqual(sorted(result), sorted(data['output']))


if __name__ == '__main__':
    unittest.main()