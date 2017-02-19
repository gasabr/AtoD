from atod.tools import parser
from atod import setup_db


heroes_list = parser.get_heroes_list()
setup_db.fill_heroes(heroes_list)
