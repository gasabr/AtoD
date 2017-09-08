import pandas as pd
from sqlalchemy.orm import sessionmaker, scoped_session

from atod.db_models import PatchModel
from atod.db import engine

session = scoped_session(sessionmaker(bind=engine))


class Member:
    ''' The parent class for all the single elements.

    Attributes:
        model (sqlalchemy.ext.declarative.api.DeclarativeMeta):
            SQlAlchemy based model which represents table in the db.
        id (int)   : unique identifier among other members.
        lvl (int)  : level of a member
        patch (str): patch for which data should be provided
    '''

    model = None

    def __init__(self, id_, lvl, patch):
        ''' Only initialise necessary attributes for any member. '''
        self._valid_arg_types(id_, lvl, patch)
        self._valid_patch(patch)

        self.id = id_
        self.lvl = lvl
        self.patch = patch

    def get_description(self):
        ''' Returns description of an object as a pd.Series. '''
        pass

    def _valid_arg_types(self, id_, lvl, patch):
        ''' Checks validness of arguments types. 
        
        Raises:
             TypeError: with all the info in message, if any of arguments
                has incorrect type.
        '''
        # check types of arguments
        if not isinstance(id_, int):
            raise TypeError('`id_` argument should be type int.')
        if not isinstance(lvl, int):
            raise TypeError('`lvl` argument should be type int.')
        if not isinstance(patch, str):
            raise TypeError('`patch` argument should be type str.')

    def _valid_patch(self, patch):
        ''' Validates patch name for further usage. 

        Args:
            patch(str): name of the patch
        
        Raises:
            ValueError: if there is no record in `patches` table with name
                equal to `patch` argument
        '''
        # if the patch value is set to default
        if patch == '':
            # there should be at least one patch
            query = session.query(PatchModel).all()
            if query[0] is None:
                # TODO: check if it is the most appropriate exception
                raise ValueError('There are no patches at all in the table,'
                                 'please, add some')

        else:
            query = session.query(PatchModel).filter(PatchModel.name == patch)
            response = query.first()

            if response is None:
               raise ValueError('There is no patch with name: {}'.format(patch))


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

    def __iter__(self):
        for m in self.members:
            yield m

    def add(self, member):
        assert type(member), self.member_type
        self.members.append(member)

    @classmethod
    def all(cls):
        ''' Creates object with all possible members. '''
        pass

    def get_list(self):
        ''' Combines all members in one data structure. '''
        data = pd.DataFrame([p.get_description(['name', 'id'])
                             for p in self.members],
                            index=[p.name for p in self.members])

        return data

    def get_description(self):
        ''' Adds properties of all the members and returns result. '''
        pass

    def __len__(self):
        return len(self.members)

    def __str__(self):
        info = '<' + self.__class__.__name__ + ' ['
        info += ''.join([str(m) + ', ' for m in self.members])
        info = info + ']>'
        return info

