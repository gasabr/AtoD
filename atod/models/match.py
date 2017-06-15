''' Class to get match description. '''
import dota2api
from YamJam import yamjam

from atod import Hero, Heroes

api = dota2api.Initialise(yamjam()['AtoD']['DOTA2_API_KEY'])


class Match(object):
    ''' Representation of the single match.

    Attributes:
        id (int)        : id of the match
        radiant (Heroes): Heroes in radiant team
        dire    (Heroes): Heroes in dire team
    '''

    def __init__(self, match_id: int):
        ''' Calls the API and creates a match representation from result.

            Args:
                match_id: Dota match ID
        '''

        self.id = match_id
        response = api.get_match_details(match_id=match_id)

        self.radiant = Heroes()
        self.dire = Heroes()

        # select picks and add heroes to appropriate teams
        for pick in filter(lambda x: x['is_pick'], response['picks_bans']):
            if pick['team'] == 0:
                self.radiant.add(Hero(pick['hero_id']))
            else:
                self.dire.add(Hero(pick['hero_id']))

    def get_description(include=[]):
        ''' Returns description of certain match.

        Description consist of 3 parts: radiant description, dire description
        and result. Complete length of description vector is 2n + 1, where
        n is a lenght of side description (depends on choosen parameters).

        Args:
            include (list, default=[]): the same with Heroes.get_description().

        '''
        pass
