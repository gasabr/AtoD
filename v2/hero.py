import json
from sqlalchemy.inspection import inspect

import settings
from setup_db import session
from dynamic_models import HeroModel

mapper = inspect(HeroModel)


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
        converter = {}
        with open(settings.CONVERTER) as fp:
            converter = json.load(fp)

        self.name = name
        self.id = converter[name]

        hero_data = session.query(HeroModel).get(self.id)

        self.columns = [column.key for column in mapper.attrs]

        for column in self.columns:
            setattr(self, column, getattr(hero_data, column))

        # add roles dictionary
        self.roles = {}
        for role, lvl in zip(self.Role.split(','), self.Rolelevels.split(',')):
            self.roles[role] = int(lvl)

    # properties
    @property
    def str(self):
        return self.AttributeBaseStrength + \
                   (self._lvl - 1) * self.AttributeStrengthGain

    @property
    def int(self):
        return self.AttributeBaseIntelligence + \
                   (self._lvl - 1) * self.AttributeAgilityGain

    @property
    def agi(self):
        return self.AttributeBaseAgility + \
                   (self._lvl - 1) * self.AttributeAgilityGain

    def __str__(self):
        return '<{name}, lvl={lvl}>'.format(name=self.name, lvl=self.lvl)
