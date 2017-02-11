from sqlalchemy.inspection import inspect

from setup_db import session
from models import HeroModel


class Hero:
    ''' Interface for HeroModel. '''

    # set of available attributes for the hero
    attributes = ()

    def __init__(self, id_):
        ''' Create hero instance by id. '''
        self.__lvl = 1
        self.__items = []
        self.__talents = []

        mapper = inspect(HeroModel)
        hero_data = session.query(HeroModel).filter(HeroModel.id == id_)[0]

        self._columns = [column.key for column in mapper.attrs]

        for column in self._columns:
            setattr(self, '__' + column, getattr(hero_data, column))

    def __str__(self):
        return '{name}, lvl={lvl}'.format(name=self.name, lvl=self.lvl)
