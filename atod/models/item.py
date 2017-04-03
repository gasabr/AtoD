from sqlalchemy import Table, Column, Integer

from atod import settings
from atod.db import Base


items = (Column(name, type_) for name, type_ in
                        settings.items_scheme.items() if name != 'ID')


class ItemModel(Base):

    __table__ = Table(settings.ITEMS_TABLE, Base.metadata,
                      Column('ID', Integer, primary_key=True),
                      *(col for col in items)
                      )

    def __init__(self, attrs):
        for key, value in attrs.items():
            setattr(self, key, value)

    def __repr__(self):
        return '<Item alias={}>'.format(self.ItemAliases)