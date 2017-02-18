#!/usr/bin/env python3
''' Setting up database. '''
import json
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import settings

engine = create_engine('sqlite:///' + settings.DB_PATH)

Base = declarative_base()
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

session = Session()
