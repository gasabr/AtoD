from datetime import datetime
from sqlalchemy import Table, Column, String, Integer, DateTime

from atod.db.setup import Base


class PatchModel(Base):

    pk      = Column(name='pk', type_=Integer, primary_key=True)
    name    = Column(name='name', type_=String)
    created = Column(name='created', type_=DateTime)

    __table__ = Table('patches', Base.metadata, 
                      pk, name, created,
                      extend_existing=True)

    def __init__(self, name):
        self.name = name
        self.created = datetime.now()

    def __repr__(self):
        return '<AbilitySpecs name={}, created={}>'.format(self.name,
                                                           self.lvl)
