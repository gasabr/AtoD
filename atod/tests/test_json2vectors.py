import json
from os import path
import unittest


from atod import settings
from atod.tools import json2vectors


EXAMPLES_FOLDER = path.join(settings.TESTS_DATA_FOLDER, 'json2vectors/')


class TestJson2Vectors(unittest.TestCase):
    def test_opening(self):
        filename = settings.ABILITIES_FILE
        # json2vectors.to_vectors(filename)

    def test_get_keys(self):
        filename = path.join(EXAMPLES_FOLDER, 'get_keys.json')
        with open(filename, 'r') as fp:
            data = json.load(fp)

        result = json2vectors.get_keys(data['input'])

        self.assertEqual(sorted(result), sorted(data['output']))


if __name__ == '__main__':
    unittest.main()
