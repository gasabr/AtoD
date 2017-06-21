import logging

from atod.db import engine
# db models
from atod.db_models import PatchModel
from atod.db_models.hero import HeroModel
from atod.db_models.ability import AbilityModel
from atod.db_models.ability_specs import  AbilitySpecsModel
from atod.db_models.ability_texts import AbilityTextsModel

logging.basicConfig(level=logging.INFO)


def create_tables():
    if not engine.has_table('patches'):
        PatchModel.__table__.create(bind=engine)
        logging.info('`patches` table was created.')

    if not engine.has_table('heroes'):
        HeroModel.__table__.create(bind=engine)
        logging.info('`heroes` table was created.')

    if not engine.has_table('abilities_specs'):
        AbilitySpecsModel.__table__.create(bind=engine)
        logging.info('`abilities_specs` was created.')

    if not engine.has_table('abilities'):
        AbilityModel.__table__.create(bind=engine)
        logging.info('`abilities` table was created.')

    if not engine.has_table('abilities_texts'):
        AbilityTextsModel.__table__.create(bind=engine)
        logging.info('`abilities_texts` table was created.')


if __name__ == '__main__':
    create_tables()
