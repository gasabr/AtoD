import json
from sqlalchemy.inspection import inspect

from atod.setup_db import session
import atod.settings as settings
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
        self.lvl = lvl
        self.items = []
        self.talents = []

        # TODO: add names to database
        # load converter since there is no names in database
        with open(settings.CONVERTER) as fp:
            converter = json.load(fp)

        self.name = name
        self.id = converter[name]

        hero_data = session.query(HeroModel).filter(HeroModel.HeroID == self.id)[0]

        self.columns = [column.key for column in mapper.attrs]

        for column in self.columns:
            setattr(self, column, getattr(hero_data, column))

        # add roles dictionary
        self.roles = {}
        for role, lvl in zip(self.Role.split(','), self.Rolelevels.split(',')):
            self.roles[role] = int(lvl)

        self.primary = PRIMARIES[self.AttributePrimary]

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

    def __str__(self):
        return '<{name}, lvl={lvl}>'.format(name=self.name, lvl=self.lvl)
