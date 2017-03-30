from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.orm import relationship

from atod import settings
from atod.utils.db.setup import Base
from atod.utils.db.create_scheme import create_abilities_scheme


class AbilityModel(Base):
    _scheme = create_abilities_scheme()
    _cols = list()

    fk_column = settings.HEROES_TABLE + '.HeroID'

    # fill list of columns
    for key, type_ in _scheme.items():
        _cols.append(Column(key, type_, nullable=True))

    _cols.append(Column('pk', settings.field_format[str],  primary_key=True))
    _cols.append(Column('HeroID', settings.field_format[int],
                        ForeignKey(fk_column)))

    # hero = relationship(settings.HEROES_TABLE)

    __table__ = Table(settings.ABILITIES_TABLE, Base.metadata,
                      *_cols)


    def __init__(self, attrs):
        self.attrs = set()
        for key, value in attrs.items():
            setattr(self, key, value)
            self.attrs.add(key)