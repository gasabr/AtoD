#!/usr/bin/env python3
''' Setting up database. '''
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import config
from models import HeroModel, Base


engine = create_engine('sqlite:///' + config.DB_PATH)

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

session = Session()


def fill_heroes(heroes_list):
    ''' Fill heroes_attr table with heroes_list. '''
    for hero in heroes_list:
        hero_model = HeroModel(**hero)
        session.add(hero_model)
        session.commit()
