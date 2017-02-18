#!/usr/bin/env python3
from sqlalchemy import Table, Column, String, Integer, Float, MetaData
from sqlalchemy.orm import mapper

from setup_db import engine, session
from db_settings import heroes_scheme

metadata = MetaData(bind=engine)

class HeroModel:
	pass

columns_gen = (Column(name, type_) for name, type_ in heroes_scheme.items())
# print(type(columns_gen()))
# for c in columns_gen:
	# print(c)

table = Table('heroes_702', metadata,
              Column('HeroID', Integer, primary_key=True),
			  *(col for col in columns_gen))

metadata.create_all()
mapper(HeroModel, table)
