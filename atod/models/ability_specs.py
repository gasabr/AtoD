import atod.db.schemas
from atod.db.setup import Base
from sqlalchemy import Table, Column, ForeignKey

from atod import settings
from atod.db.schemas import get_ability_specs_schema


class AbilitySpecsModel(Base):
    _scheme = get_ability_specs_schema()
    _cols = list()

    fk_column = settings.HEROES_TABLE + '.HeroID'

    # fill list of columns
    for key, type_ in _scheme.items():
        _cols.append(Column(key, type_, nullable=True))

    _cols.append(Column('pk', atod.db.schemas.field_format[str],
                        primary_key=True))
    _cols.append(Column('HeroID', atod.db.schemas.field_format[int],
                        ForeignKey(fk_column)))

    __table__ = Table(settings.ABILITIES_SPECS_TABLE, Base.metadata,
                      *_cols)

    def __init__(self, attrs):
        self.attrs = set()
        for key, value in attrs.items():
            setattr(self, key, value)
            self.attrs.add(key)

    def __repr__(self):
        return '<AbilitySpecs name={}, lvl={}>'.format(self.name, self.lvl)