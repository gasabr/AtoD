from sqlalchemy import Table, Column, Integer

from atod import settings
from atod.db import Base
from atod.db.schemas import create_heroes_scheme

heroes = (Column(n, t) for n, t
          in create_heroes_scheme().items() if n != 'HeroID')

class HeroModel(Base):

    __table__ = Table(settings.HEROES_TABLE, Base.metadata,
                      Column('HeroID', Integer, primary_key=True,
                             autoincrement=False),
                             *(col for col in heroes))

    def __init__(self, attrs):
        self.attrs = set()
        for key, value in attrs.items():
            setattr(self, key, value)
            self.attrs.add(key)

    def __repr__(self):
        return '<HeroModel::{}>'.format(self.name)