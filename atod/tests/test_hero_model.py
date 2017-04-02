import unittest

from atod import session
from atod.models import HeroModel


class MyTestCase(unittest.TestCase):

    def test_attributes(self):
        for row in session.query(HeroModel).all():
            self.assertEqual(False, hasattr(row, 'url'))
            self.assertEqual(True, hasattr(row, 'name'))
            self.assertEqual(True, hasattr(row, 'in_game_name'))


if __name__ == '__main__':
    unittest.main()
