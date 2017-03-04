import json
from os import path
import unittest

from atod import settings
from atod.tools import json2vectors


EXAMPLES_FOLDER = path.join(settings.TESTS_DATA_FOLDER, 'json2vectors/')


class TestJson2Vectors(unittest.TestCase):
    pass

if __name__ == '__main__':
    unittest.main()
