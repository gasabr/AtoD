from sqlalchemy.orm import sessionmaker, scoped_session

from atod.db import engine

session = scoped_session(sessionmaker(bind=engine))


class CommonTable:
    ''' Defines common for all the tables operations. '''

    @classmethod
    def delete(cls, **kwargs):
        ''' Removes all the records where column (kwarg key) equal value. 
        
        Args:
            kwargs: pairs column-value records with which should be removed.

        '''
        rows = session.query(cls).filter_by(**kwargs).all() 
        for row in rows:
            session.delete(row)
        session.commit()
        
