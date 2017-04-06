''' This is an interface for any class which describes group of something. 

    It can be Heroes, Abilities, Items or somethings else. 
'''

class Group:

    # items mean containde
    members = list()

    def add(self, member):
        self.members.append(member)

    def remove(self, member):
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