import json
from os import path
import unittest


from atod import settings
from atod.tools import json2vectors


EXAMPLES_FOLDER = path.join(settings.TESTS_DATA_FOLDER, 'json2vectors/')


class TestJson2Vectors(unittest.TestCase):

    # FIXME: all the test doesn't cover case where input looks like this:
    # {
    #   "gloval_key": {
    #       "Version": "1",
    #       "normal_key": {...}
    #   }
    # }
    # Have to get rid of all the keys which are mapped not to dictionaries

    def test_get_keys(self):
        filename = path.join(EXAMPLES_FOLDER, 'get_keys.json')
        with open(filename, 'r') as fp:
            data = json.load(fp)

        result = json2vectors.get_keys(data['input'])

        self.assertEqual(sorted(result), sorted(data['output']))

    def test_make_flat_dict(self):
        filename = path.join(EXAMPLES_FOLDER, 'make_flat_dict.json')
        with open(filename, 'r') as fp:
            data = json.load(fp)

        result = json2vectors.make_flat_dict(data['input'])

        self.assertEqual(result, data['output'])

    def test_to_vectors(self):
        frame = json2vectors.to_vectors(settings.ABILITIES_FILE)

        print(frame.shape)

        frame = frame.dropna(0, thresh=3)
        frame = frame.dropna(1, 'all')

        print(frame.shape)


if __name__ == '__main__':
    unittest.main()
