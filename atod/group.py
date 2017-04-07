''' This is an interface for any class which describes group of something. 

    It can be Heroes, Abilities, Items or somethings else. 
'''

from atod.db import session

class Group:

    members = list()

    def __init__(self, members):
        member_type = type(members[0]) if len(members) > 0 else None
        for m in members:
            # members of different types are not allowed
            assert member_type, type(m)
            self.members.append(m)

    def add(self, member):
        self.members.append(member)

    def remove(self, member_name):
        pass

    def combine(self):
        ''' Combine properties of items.'''
        pass

    def compare(self):
        ''' Compare items. '''
        pass

    def as_vector(self):
        ''' Return a math vector representation. '''
        pass

    def __getitem__(self, member):
        for m in self.members:
            if m.name == member:
                return m

        return None

    def __str__(self):
        info = '<' + self.__class__.__name__ + ' ['
        info += ''.join([str(m) + ', ' for m in self.members])
        info = info + ']>'
        return info


class Member:

    # in every
    model = None

    def __init__(self, id_=None, name=None):
        # check if user has set up model attribute
        if self.model is None:
            class_name = self.__class__.__name__
            raise ValueError('Please set up model for {}', format(class_name))

        # search row in model where id or name equal to `create_from`
        res = session.query(self.model).filter(self.model.id == id_).all()

        # if not self._valid_input_dict(input_dict):
        #     raise ValueError('Invalid input dictionary.')
        #
        # member_as_dict = input_dict.copy()
        # self.lvl  = 0
        # self.id   = member_as_dict['id']
        # self.name = member_as_dict['name']
        #
        # del member_as_dict['id']
        # del member_as_dict['name']
        #
        # self.specs = member_as_dict

    def _valid_input_dict(self, dict_):
        ''' Check validness of input dictionary in init method. 
        
            Returns:
                True / False: False if dict_ is not a dict, or it doesn't
                    contain `name` key.
        '''
        if not isinstance(dict_, dict):
            return False

        if 'name' not in dict_:
            return False

        return True

    def as_dict(self):
        pass