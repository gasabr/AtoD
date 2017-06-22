import unittest
from atod import Ability


class TestAbility(unittest.TestCase):
    def test_init(self):
        # create ability with non existent id
        self.assertRaises(ValueError, Ability, 14)
        self.assertRaises(TypeError, Ability, 11, 1.0)
        self.assertRaises(TypeError, Ability, 11, 5, 706)


if __name__ == '__main__':
    unittest.main()
