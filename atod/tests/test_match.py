import unittest
import dota2api

from atod import Match, Hero


class TestMatch(unittest.TestCase):

    def setUp(self):
        self.all_random_match_id = 3430968846
        self.captain_mode_match_id = 3430944845
        
    def test_init_invalid_game_mode(self):
        ''' Tests init method with valid id, which is not supported for now.  '''
        self.assertRaises(
                NotImplementedError,
                Match, self.all_random_match_id, 
                )

    def test_init_valid_game_mode(self):
        ''' Tests init method with integer which should not raise anything. '''
        self.assertIsInstance(
                Match(self.captain_mode_match_id), 
                Match
                )

    def test_init_with_string_id(self):
        ''' Test init method with invalid match_id type. '''
        string_match_id = 'sdasdasdasd'

        self.assertRaises(
                TypeError,
                Match, string_match_id,
                )

    def test_init_with_practice_match_id(self):
        ''' `match_id` is valid, but API should raise an exception. 
        
        It's impossible to check if random int is practice match or not
        without calling API, but if it it API will return error. 
        '''
        practice_match_id = 100

        self.assertRaises(
                dota2api.src.exceptions.APIError,
                Match, practice_match_id,
                )

    def test_description_shape(self):
        ''' Tests different way.
        
        Ideally this test should check all possible arguments in include.
        '''
        # what should be included in both descriptions
        include = ['role']

        # get random hero description
        hero = Hero(1)
        hero_desc = hero.get_description(include)

        # get match description
        match = Match(self.captain_mode_match_id)
        match_desc = match.get_description(include)

        # length of match description should be 2n + 1, where
        # n is length of hero description for given category.
        self.assertEqual(hero_desc.shape[0] * 2 + 1, match_desc.shape[0])

