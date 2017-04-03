import json

from sqlalchemy.inspection import inspect

import atod.settings as settings
from atod.abilities import abilities as Abilities
from atod.db import session
from atod.models import HeroModel

mapper = inspect(HeroModel)

PRIMARIES = {
    'DOTA_ATTRIBUTE_AGILITY': 'agility',
    'DOTA_ATTRIBUTE_STRENGTH': 'strength',
    'DOTA_ATTRIBUTE_INTELLECT': 'intellect',
}


class Hero(object):
    ''' Interface for HeroModel. '''

    def __init__(self, name, lvl=1):
        ''' Create hero instance by id. '''
        # TODO: create metaclass to prevent changing this variables
        #       or just create properties
        self.lvl = lvl
        self.items = []
        self.talents = []

        # TODO: add names to database
        # load converter since there is no names in database
        with open(settings.CONVERTER) as fp:
            converter = json.load(fp)

        with open(settings.IN_GAME_CONVERTER) as fp:
            in_game_converter = json.load(fp)

        self.name = name
        self.id = converter[name]
        self.in_game_name = in_game_converter[str(self.id)]

        hero_data = session.query(HeroModel).filter(
            HeroModel.HeroID == self.id)[0]

        self.columns = [column.key for column in mapper.attrs]

        for column in self.columns:
            setattr(self, column, getattr(hero_data, column))

        # add roles dictionary
        self.roles = {}
        for role, lvl in zip(self.Role.split(','), self.Rolelevels.split(',')):
            self.roles[role] = int(lvl)

        self.primary = PRIMARIES[self.AttributePrimary]

        self.abilities = Abilities.filter(hero=self.in_game_name)

    # properties
    @property
    def str(self):
        return self.AttributeBaseStrength + \
                   (self.lvl - 1) * self.AttributeStrengthGain

    @property
    def int(self):
        return self.AttributeBaseIntelligence + \
                   (self.lvl - 1) * self.AttributeAgilityGain

    @property
    def agi(self):
        return self.AttributeBaseAgility + \
                   (self.lvl - 1) * self.AttributeAgilityGain

    # TODO: this should be property with setter
    def abilities_labels(self):
        '''Returns dictionary ability->labels.'''
        labels = {}
        for a in self.abilities:
            labels[a.raw_name] = a.labels

        return labels

    def has(self, effect):
        for ability, labels in self.abilities_labels().items():
            if effect in labels:
                return True

        return False

    def __str__(self):
        return '<{name}, lvl={lvl}>'.format(name=self.name, lvl=self.lvl)
