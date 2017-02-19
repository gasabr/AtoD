#!/usr/bin/env python3
from sqlalchemy import Table, Column, String, Integer, Float, MetaData
from sqlalchemy.orm import mapper

from setup_db import engine, session, Base
import settings


heroes = (Column(n, t) for n, t in settings.heroes_scheme.items())
items = (Column(name, type_) for name, type_ in
                        settings.items_scheme.items() if name != 'ID')

class HeroModel(Base):

    __table__ = Table('heroes_' + settings.CURRENT_VERSION, Base.metadata,
                      Column('HeroID', Integer, primary_key=True),
    			      *(col for col in heroes),            
                      )

    def __init__(self, attrs):
        self.attrs = set()
        for key, value in attrs.items():
            setattr(self, key, value)
            self.attrs.add(key)


class ItemModel(Base):

    __table__ = Table('items_' + settings.CURRENT_VERSION, Base.metadata,
                      Column('ID', Integer, primary_key=True),
                      *(col for col in items)
                      )

    def __init__(self, attrs):
        for key, value in attrs.items():
            setattr(self, key, value)


def create_tables():
    Base.metadata.create_all(engine)
