''' This modulde contains tools for any DB-related tasks. 

If you want to use `session`, please, use scoped version, it's needed to
ensure thread-safety (or, it's also possible, I'm using SQLAlchemy not
entirely right).
'''
from .setup import Base, engine
from .create_tables import create_tables
