import pandas as pd

from atod import Ability
from atod.db import session
from atod.db_models.ability import AbilityModel
from atod.db_models.ability_texts import AbilityTextsModel
from atod.models.interfaces import Group


class Abilities(Group):

    member_type = Ability

    # TODO: write version with levels arguments
    @classmethod
    def from_hero_id(cls, HeroID, patch=''):
        ''' Adds to members all abilities of the hero with `HeroID`. '''
        response = session.query(AbilityModel.ID)
        response = response.filter(AbilityModel.HeroID == HeroID).all()

        if len(response) == 0:
            report = 'No abilities for this HeroID == {}'.format(HeroID)
            raise ValueError(report)

        members_ = [cls.member_type(a[0], patch=patch) for a in response]

        return cls(members_)

    # TODO: this can be generalized with `member_type.model.ID`
    @classmethod
    def all(cls):
        ''' Creates Abilities object with all heroes abilities in the game.'''
        ids = [x[0] for x in session.query(AbilityModel.ID).all()]
        # XXX: would be nice to create members only if they are needed
        members_ = [Ability(id_) for id_ in ids]

        return cls(members_)

    def get_description(self, include):
        '''
        Possible options for `include`:
        * labels
        * specs
        
        You can't get texts with this function, because it would break idea:
        this function is to get information about *all* members combined, but
        if you want to get independent info for each member - call desired
        function on each member.
        
        Args:
            include: list
        
        Returns:

        '''
        pass

    def get_list(self, include: list):
        ''' Returns information about members in the form: row is a member.

            'List' because descriptions are just concatenated with each other,
            but not summed by any means.

            Returns:
                pd.DataFrame: shape=(len(self.members),
                    len(<member description>)). Rows are abilities, columns -
                    their properties. Labels columns names start with
                    'label_'.
        '''

        # get all descriptions
        descriptions = [m.get_description(include) for m in self.members]

        return pd.DataFrame(descriptions, columns=descriptions[0].index,
                            index=None)

    def get_specs_list(self, include=[]):
        ''' Returns list of all member's descriptions (ONLY specs part).

            Returns:
                pd.DataFrame: shape=(len(members), len(<member description>)).
                    Rows are abilities, columns - their properties.
                    Labels columns names start with 'label_'.
        '''

        # get all descriptions
        descriptions = [m.get_specs(include) for m in self.members]

        return pd.DataFrame(descriptions, columns=descriptions[0].index,
                            index=None)

    def get_labels_list(self):
        ''' Returns list of all member's descriptions (ONLY specs part).

            Returns:
                pd.DataFrame: shape=(len(members), len(<member description>)).
                    Rows are abilities, columns - their properties.
                    Labels columns names start with 'label_'.
        '''

        # get all descriptions
        descriptions = [m.get_labels() for m in self.members]

        return pd.DataFrame(descriptions, columns=descriptions[0].index)

    def get_texts(self):
        ''' Returns:
                pd.DataFrame: texts of abilities in DataFrame.
        '''

        # get members ids
        members_ids = [m.id for m in self.members]
        # get all texts
        all_texts = session.query(AbilityTextsModel).all()
        # find texts for members by ids
        members_texts = [row for row in all_texts
                         if any(map(lambda x: row.ID == x, members_ids))]

        # create DataFrame from chosen rows
        texts = pd.DataFrame([m.__dict__ for m in members_texts])
        texts = texts.drop(['_sa_instance_state'], axis=1)

        return texts

    def get_summary(self):
        ''' Sums up all labels of members (they are binary decoded).

            Returns:
                pd.Series:
        '''

        labels_list = self.get_labels_list()
        summary = labels_list.sum(axis=0)
        del summary['name']

        return summary
