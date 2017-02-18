#!/usr/bin/env python3
from sqlalchemy import Table, Column, String, Integer, Float, MetaData
from sqlalchemy.orm import mapper

from setup_db import engine, session
from settings import heroes_scheme

metadata = MetaData(bind=engine)

class HeroModel:

    def __init__(self, attrs):
        self.attrs = ()
        for key, value in attrs.items():
            setattr(self, key, value)
            self.attrs.add(key)

columns_gen = (Column(name, type_) for name, type_ in heroes_scheme.items())

# create a table to map HeroModel
table = Table('heroes_702', metadata,
              Column('HeroID', Integer, primary_key=True),
			  *(col for col in columns_gen))

metadata.create_all()
mapper(HeroModel, table)
