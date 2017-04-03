from sqlalchemy import Table, Column, Integer, String, ForeignKey

from atod import settings
from atod.db import Base


class AbilityModel(Base):

    _cols = [Column(label, Integer) for label in settings.LABELS]
    _cols.append(Column('ID', Integer, primary_key=True))
    _cols.append(Column('name', String))

    # foreign key to this column
    fk_heroes = settings.HEROES_TABLE + '.HeroID'
    _cols.append(Column('HeroID', Integer, ForeignKey(fk_heroes)))

    __table__ = Table(settings.ABILITIES_TABLE, Base.metadata,
                      *_cols)

    def __init__(self, attrs):
        self.attrs = set()
        for key, value in attrs.items():
            setattr(self, key, value)
            self.attrs.add(key)

    def __repr__(self):
        return '<AbilityModel::{}>'.format(self.name)