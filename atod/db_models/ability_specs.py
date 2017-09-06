from sqlalchemy import Table, Column

from atod.db.setup import Base
from atod.db.schemas import get_abilities_specs_schema
from atod.db_models.common_table import CommonTable


class AbilitySpecsModel(Base, CommonTable):

    _cols = [Column(**col) for col in get_abilities_specs_schema()]

    __table__ = Table('abilities_specs', Base.metadata, *_cols)

    def __init__(self, attrs):
        self.attrs = set()
        for key, value in attrs.items():
            setattr(self, key, value)
            self.attrs.add(key)

    def __repr__(self):
        return '<AbilitySpecs name={}, lvl={}>'.format(self.name, self.lvl)
