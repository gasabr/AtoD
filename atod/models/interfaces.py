import pandas as pd

from atod.db import session


class Member:
    ''' The parent class for all the single elements.

        Attributes:
            model (sqlalchemy.ext.declarative.api.DeclarativeMeta):
                SQlAlchemy based model which represents table in the db.
            id (int)  : unique identifier among other members.
    '''

    model = None

    def __init__(self, id_):
        ''' Only initialise necessary attributes for any member. '''
        self.id = id_

    def get_description(self):
        ''' Returns a object as a pd.Series.

            Returns:
                vector (pandas.Series): representation of the object

        '''
        pass

    def as_dict(self):
        ''' Returns representation of this object as a dictionary.'''
        return dict()


class Group:
    ''' Represents abstract set of members.

        Attributes:
            member_type (class): the type of member
            members (list)     : list of objects of class `member_type`
    '''

    member_type = Member

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

    @classmethod
    def all(cls):
        ''' Creates object with all possible members. '''
        pass

    def remove(self, member_name):
        pass

    def compare(self):
        ''' Compare items. '''
        pass

    def get_list(self):
        ''' Combines all members in one data structure. '''
        data = pd.DataFrame([p.get_description() for p in self.members],
                            index=[p.name for p in self.members])

        return data

    def get_summary(self):
        ''' Adds properties of all the members and returns result. '''
        pass

    def __getitem__(self, item):
        return self.members[item]

    def __len__(self):
        return len(self.members)

    def __str__(self):
        info = '<' + self.__class__.__name__ + ' ['
        info += ''.join([str(m) + ', ' for m in self.members])
        info = info + ']>'
        return info
