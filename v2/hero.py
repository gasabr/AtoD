import json
from sqlalchemy.inspection import inspect

import settings
from setup_db import session
from dynamic_models import HeroModel


class Hero:
    ''' Interface for HeroModel. '''

    # set of available attributes for the hero
    attributes = ()

    def __init__(self, id_):
        ''' Create hero instance by id. '''
        self.__lvl = 1
        self.__items = []
        self.__talents = []

        heroes_features = {}
        with open(settings.ID_TO_NAME) as fp:
            heroes_features = json.load(fp)

        self._name = heroes_features[str(id_)]['name']

        mapper = inspect(HeroModel)
        hero_data = session.query(HeroModel).filter(HeroModel.HeroID == id_)[0]

        self._columns = [column.key for column in mapper.attrs]

        for column in self._columns:
            setattr(self, column, getattr(hero_data, column))

    def __str__(self):
        return '{id}, lvl={lvl}'.format(id=self.HeroID, lvl=self.lvl)
