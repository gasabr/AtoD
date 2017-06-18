from sqlalchemy import Table, Column

from atod.db import Base
from atod import meta_info
from atod.db.schemas import get_abilities_schema


class AbilityModel(Base):

    _cols = [Column(**col) for col in get_abilities_schema()]

    __table__ = Table(meta_info.get_tables_prefix() + 'abilities',
                      Base.metadata, *_cols)

    def __init__(self, attrs):
        self.attrs = set()
        for key, value in attrs.items():
            setattr(self, key, value)
            self.attrs.add(key)

    def __repr__(self):
        return '<AbilityModel::{}>'.format(self.name)
