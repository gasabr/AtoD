from sqlalchemy.orm import sessionmaker, scoped_session

from atod.db import engine, create_tables
from atod.db_models.patch import PatchModel

session = scoped_session(sessionmaker(bind=engine))


class Meta(object):
    ''' Class stores meta information about versions. '''

    def __init__(self):
        ''' Finds the last created version and set up lib to use it. '''
        create_tables()

        query = session.query(PatchModel.name).order_by(
                    PatchModel.created).first()

        if query is not None:
            self._patch_name = query[0]
        else:
            print('There is no data in the db, please add at least one patch.\n'
                  'see `atod.utils.update.add_patch()` on how to make it ')
            self._patch_name = ''

    @property
    def patch(self):
        return self._patch_name

    def set_patch(self, name: str):
        # check if the patch is created in the db
        patches = [p[0] for p in session.query(PatchModel.name).all()]

        if name not in patches:
            raise ValueError('Please, create a record in `patches` table'
                             'before using the patch.')

        self._patch_name = name

meta_info = Meta()
