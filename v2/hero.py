import json
from sqlalchemy.inspection import inspect

import settings
from setup_db import session
from dynamic_models import HeroModel


class Hero:
    ''' Interface for HeroModel. '''

    # set of available attributes for the hero
    attributes = ()

    def __init__(self, name, lvl=1):
        ''' Create hero instance by id. '''
        # TODO: create metaclass to prevent changing this variables
        self.__lvl = lvl
        self.__items = []
        self.__talents = []

        # TODO: add names to database
        # load converter since there is no names in database
        converter = {}
        with open(settings.CONVERTER) as fp:
            converter = json.load(fp)

        self.name = name
        self._id = converter[name]

        mapper = inspect(HeroModel)
        # TODO: change it to get_by or something like that, not filter
        response = session.query(HeroModel).filter(HeroModel.HeroID == self._id)
        hero_data = response[0]

        self._columns = [column.key for column in mapper.attrs]

        for column in self._columns:
            setattr(self, '_' + column, getattr(hero_data, column))

        # XXX: is that the right way?
        self.str = self._AttributeBaseStrength + \
                   (lvl-1) * self._AttributeStrengthGain
        self.agi = self._AttributeBaseAgility + \
                   (lvl-1) * self._AttributeAgilityGain
        self.int = self._AttributeBaseIntelligence + \
                   (lvl-1) * self._AttributeIntelligenceGain

    def __str__(self):
        return '{name}, lvl={lvl}'.format(name=self._name, lvl=self.lvl)

    def atrributes(self):
        return ''
