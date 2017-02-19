#!/usr/bin/env python3
from sqlalchemy import Table, Column, String, Integer, Float, MetaData
from sqlalchemy.orm import mapper

from setup_db import engine, session
import settings

metadata = MetaData(bind=engine)

class HeroModel:

    def __init__(self, attrs):
        self.attrs = ()
        for key, value in attrs.items():
            setattr(self, key, value)
            self.attrs.add(key)

def create_heroes_table():
    # n-name and t-type
    heroes = (Column(n, t) for n, t in settings.heroes_scheme.items())

    # create a table to map HeroModel
    heroes_table = Table('heroes_' + settings.CURRENT_VERSION, metadata,
                         Column('HeroID', Integer, primary_key=True),
    			         *(col for col in heroes),
                         )
    mapper(HeroModel, heroes_table)

class ItemModel:

    def __init__(self, attrs):
        self.attrs = ()
        for key, value in attrs.items():
            setattr(self, key, value)
            self.attrs.add(key)


def create_items_table():
    # exclude id from columns since it would be added as primary_key
    items = (Column(name, type_) for name, type_ in
                        settings.items_scheme.items() if name != 'ID')

    items_table = Table('items_' + settings.CURRENT_VERSION, metadata,
                        Column('ID', Integer, primary_key=True),
                        *(col for col in items)
                        )

    mapper(ItemModel, items_table)

# create_heroes_table()
create_items_table()
metadata.create_all()
session.commit()
