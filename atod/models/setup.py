#!/usr/bin/env python3
from atod.utils.db.setup_db import Base, engine


def create_tables():
    Base.metadata.create_all(engine)
