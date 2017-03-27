from sqlalchemy import Table, Column, Integer

from atod import settings
from atod.utils.db.setup_db import Base

heroes = (Column(n, t) for n, t
          in settings.heroes_scheme.items() if n != 'HeroID')

class HeroModel(Base):

    __table__ = Table('heroes_' + settings.CURRENT_VERSION, Base.metadata,
                      Column('HeroID', Integer, primary_key=True,
                             autoincrement=False),
                             *(col for col in heroes),
                      )

    def __init__(self, attrs):
        self.attrs = set()
        for key, value in attrs.items():
            setattr(self, key, value)
            self.attrs.add(key)