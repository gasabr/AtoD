from sqlalchemy import Table, Column, Integer, String

from atod.db.setup import Base


class AbilityTextsModel(Base):

    ID          = Column(name='ID', type_=Integer, primary_key=True,
                         autoincrement=False)
    name        = Column(name='name', type_=String)
    lore        = Column(name='lore', type_=String, nullable=True)
    description = Column(name='description', type_=String)
    notes       = Column(name='notes', type_=String)
    other       = Column(name='other', type_=String, nullable=True)

    __table__ = Table('abilities_texts', Base.metadata,
                      ID, name, lore, description, notes, other)

    def __init__(self, attrs):
        self.attrs = set()
        for key, value in attrs.items():
            setattr(self, key, value)
            self.attrs.add(key)

    def __repr__(self):
        return '<AbilityTexts name={}>'.format(self.name)
