#!/usr/bin/env python3
''' Setting up database. '''
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from atod import settings

engine = create_engine('sqlite:///' + settings.DB_PATH)

Base = declarative_base()
Session = sessionmaker(bind=engine)

session = Session()
