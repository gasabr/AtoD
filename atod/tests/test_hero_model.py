import unittest
from sqlalchemy.orm import sessionmaker, scoped_session

from atod.db import engine
from atod.db_models.hero import HeroModel

session = scoped_session(sessionmaker(bind=engine))


class MyTestCase(unittest.TestCase):

    def test_attributes(self):
        for row in session.query(HeroModel).all():
            self.assertEqual(False, hasattr(row, 'url'))
            self.assertEqual(True, hasattr(row, 'name'))
            self.assertEqual(True, hasattr(row, 'in_game_name'))


if __name__ == '__main__':
    unittest.main()
