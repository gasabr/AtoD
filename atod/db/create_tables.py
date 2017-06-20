import logging

from atod import settings
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

    if not engine.has_table(settings.HEROES_TABLE):
        HeroModel.__table__.create(bind=engine)
        logging.info(settings.HEROES_TABLE + ' was created.')

    if not engine.has_table(settings.ABILITIES_SPECS_TABLE):
        AbilitySpecsModel.__table__.create(bind=engine)
        logging.info(settings.ABILITIES_SPECS_TABLE + ' was created.')

    if not engine.has_table(settings.ABILITIES_TABLE):
        AbilityModel.__table__.create(bind=engine)
        logging.info(settings.ABILITIES_TABLE + ' was created.')

    if not engine.has_table(settings.ABILITIES_TEXTS_TABLE):
        AbilityTextsModel.__table__.create(bind=engine)
        logging.info(settings.ABILITIES_TEXTS_TABLE + ' was created.')


if __name__ == '__main__':
    create_tables()
