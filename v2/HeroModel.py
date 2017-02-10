from sqlalchemy import Column, String, Integer, Float
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class HeroModel(object):
    ''' Table to store heroes and their attributes. 
    
        All the information from is parsed from config.HEROES_TABLE_URL,
        except legs and collision :)
        *_base means at the start of the game without any items.
    '''

    __tablename__ = 'Heroes_701'

    # Columns:
    id           = Column(Integer)
    primary_attr = Column(Integer) # scheme: config.primary_attr_to_int
    str_base     = Column(Integer)
    str_gain     = Column(Float)
    agi_base     = Column(Integer)
    agi_gain     = Column(Float)
    int_base     = Column(Integer)
    int_gain     = Column(Float)
    total        = Column(Integer)
    total_gain   = Column(Float)
    total_lvl25  = Column(Float)
    mov_speed    = Column(Integer)
    armor_base   = Column(Float)
    dmg_base_min = Column(Integer)
    dmg_base_max = Column(Integer)
    range        = Column(Integer)
    vision_day   = Column(Integer)
    vision_night = Column(Integer)
    attack_point = Column(Integer)
    attack_base_time  = Column(Float)
    hp_regen_base     = Column(Float)
    turn_rate         = Column(Float)
    # TODO: add mp_regen_base = Cloumns(Float)
    # TODO: add magic_resistance