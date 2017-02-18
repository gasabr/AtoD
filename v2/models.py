#!/usr/bin/env python3
from sqlalchemy import Column, String, Integer, Float
# from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base        


Base = declarative_base()

class HeroMeta(type):

    def __init__(cls, clsname, superclasses, attributedict):
        for attr_name, attr_type in scheme.items():
            print('wow')
            # setattr(cls, attr_name, Column(attr_type))
            setattr(cls, attr_name, attr_type)


class HeroModel(Base):
    ''' Table to store heroes and their attributes.

        All the information from is parsed from settings.HEROES_TABLE_URL,
        except legs and collision
        *_base means at the start of the game without any items.
    '''
    columns = [Column(attr_type)]
    # __columns = [key for key, value in scheme.items()]

    # Columns:
    HeroID = Column(Integer, primary_key=True)

    # def __new__(cls):
    #     for attr_name, attr_type in scheme.items():
    #         setattr(cls, attr_name, Column(attr_type))
    # name         = Column(String(32))
    # legs         = Column(Integer)
    # primary_attr = Column(Integer) # scheme: settings.primary_attr_to_int
    # str_base     = Column(Integer)
    # str_gain     = Column(Float)
    # agi_base     = Column(Integer)
    # agi_gain     = Column(Float)
    # int_base     = Column(Integer)
    # int_gain     = Column(Float)
    # total        = Column(Integer)
    # total_gain   = Column(Float)
    # total_lvl25  = Column(Float)
    # mov_speed    = Column(Integer)
    # armor_base   = Column(Float)
    # dmg_base_min = Column(Integer)
    # dmg_base_max = Column(Integer)
    # range        = Column(Integer)
    # vision_day   = Column(Integer)
    # vision_night = Column(Integer)
    # attack_point = Column(Integer)
    # collision    = Column(Integer)
    # attack_time_base  = Column(Float)
    # attack_backswing  = Column(Float)
    # hp_regen_base     = Column(Float)
    # turn_rate         = Column(Float)
    # TODO: add mp_regen_base = Cloumns(Float)
    # TODO: add magic_resistance

    def columns(self):
        return self.__columns
