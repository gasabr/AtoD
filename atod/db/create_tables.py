import logging

from atod import settings
from atod.db import engine
from atod.models import (AbilitySpecsModel, HeroModel, AbilityModel,
                         AbilityTextsModel)

logging.basicConfig(level=logging.INFO)


def create_tables():
    if not engine.has_table(settings.HEROES_TABLE):
        HeroModel.__table__.create(bind=engine)
        logging.info(settings.HEROES_TABLE + ' was created.')

    # items are excluded from the program for some time
    # if not engine.has_table(settings.ITEMS_TABLE):
    #     ItemModel.__table__.create(bind=engine)
    #     logging.info(settings.ITEMS_TABLE + ' was created.')

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