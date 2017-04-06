''' This module describes single hero ability.'''
import json

from atod import settings
from atod.group import Group
from atod.models import AbilityModel, AbilitySpecsModel


class Abilities(Group):
    pass


class Ability:
    '''Wrapper for raw json data from Abilities.'''

    def __init__(self, name, description):
        self.id = description['ID']
        self.raw_name = name
        self.lvl = 0

        for key in description:
            k = key
            if key.startswith('Ability'):
                k = key[7:]
            setattr(self, k.lower(), description[key])

        with open(settings.ABILITIES_LABELING_FILE, 'r') as fp:
            self.labels = list(set(json.load(fp)[self.raw_name]))


    def __str__(self):
        return '<Ability name={}, lvl={}>'.format(self.raw_name, self.lvl)

    def __repr__(self):
        return '<Ability name={}, lvl={}>'.format(self.raw_name, self.lvl)

    def __getattr__(self, item):
        return getattr(self, item)
