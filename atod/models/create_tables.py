from atod import settings
from atod.utils.db.setup import engine
from atod.models import AbilityModel, HeroModel, ItemModel


def create_tables():
    if not engine.has_table(settings.HEROES_TABLE):
        HeroModel.__table__.create(bind=engine)
    if not engine.has_table(settings.ITEMS_TABLE):
        ItemModel.__table__.create(bind=engine)
    if not engine.has_table(settings.ABILITIES_TABLE):
        AbilityModel.__table__.create(bind=engine)


if __name__ == '__main__':
    create_tables()