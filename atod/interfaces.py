''' This is an interface for any class which describes group of something. 

    It can be Heroes, Abilities, Items or somethings else. 
'''
import pandas as pd

from atod.db import session

class Group:

    member_type = None

    def __init__(self, i_members=[]):
        # check if user has set up `model` attribute
        if self.member_type is None:
            class_name = self.__class__.__name__
            raise ValueError('Please set up member_type for ' + class_name)

        # verify members types and add them into members
        self.members = list()
        for m in i_members:
            assert type(m), self.member_type
            self.members.append(m)

    def add(self, member):
        assert type(member), self.member_type
        self.members.append(member)

    def _all(self):
        ''' Returns all the records from member's table in db. '''
        member_model = self.member_type.model
        response = session.query(member_model).all()
        return [self.member_type(m) for m in response]

    def remove(self, member_name):
        pass

    def combine(self):
        ''' Combine properties of items.'''
        pass

    def compare(self):
        ''' Compare items. '''
        pass

    def to_dataframe(self):
        data = pd.DataFrame([p.to_series() for p in self.members],
                            index=[p.name for p in self.members])

        return data

    def __getitem__(self, item):
        return self.members[item]

    def __len__(self):
        return len(self.members)

    def __str__(self):
        info = '<' + self.__class__.__name__ + ' ['
        info += ''.join([str(m) + ', ' for m in self.members])
        info = info + ']>'
        return info


class Member:

    model = None

    def __init__(self, id_, name):
        ''' Only initialise necessary attributes for any member. '''
        self.id   = id_
        self.name = name

    def to_series(self):
        ''' Returns a object as a pd.Series. 

            Returns:
                vector (pandas.Series): representation of the object

        '''
        pass

    def _dict2vector(self, specs):
        ''' Creates pandas.Series from dictionary with the rules below.

            Args:
                specs (dict): information to create Series    

        '''
        pass

    def as_dict(self):
        ''' Returns representation of this object as a dictionary.'''
        return dict()