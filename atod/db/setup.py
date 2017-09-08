#!/usr/bin/env python3
''' Setting up database. '''
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from atod import files

engine = create_engine('sqlite:///' + files.DB_PATH)

Base = declarative_base()
Session = sessionmaker(bind=engine)
