from sqlalchemy import Table, Column

from atod.db import Base
from atod.db.schemas import get_heroes_schema


class HeroModel(Base):

    heroes = (Column(**col) for col in get_heroes_schema())

    __table__ = Table('heroes', Base.metadata, *heroes)

    def __init__(self, attrs):
        self.attrs = set()
        for key, value in attrs.items():
            setattr(self, key, value)
            self.attrs.add(key)

    def __repr__(self):
        return '<HeroModel::{}>'.format(self.name)
