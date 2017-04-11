from sqlalchemy.inspection import inspect

from atod.db import session
from atod.models import HeroModel
from atod.abilities import Abilities
from atod.interfaces import Group, Member

mapper = inspect(HeroModel)

PRIMARIES = {
    'DOTA_ATTRIBUTE_AGILITY': 'agility',
    'DOTA_ATTRIBUTE_STRENGTH': 'strength',
    'DOTA_ATTRIBUTE_INTELLECT': 'intellect',
}


class Hero(Member):
    ''' Interface for HeroModel. '''

    base_health = 200
    base_health_regen = 0.25
    base_mana = 50
    base_mana_regen = 0.01
    base_damage = 21
    base_armor = -1

    def __init__(self, id_):
        query = session.query(HeroModel)
        specs = query.filter(HeroModel.HeroID == id_).first()
        super().__init__(specs.HeroID, specs.name)

        self.in_game_name = specs.in_game_name
        del specs.__dict__['name']
        del specs.__dict__['in_game_name']

        self.lvl = 1
        self.specs = specs.__dict__
        self.abilities = Abilities.from_hero_id(self.id)

    @classmethod
    def from_name(cls, name):
        ''' Converts name to id with and calls init. 
        
            Raises:
                ValueError: if `name` is not in heroes.name column
        '''
        query = session.query(HeroModel.HeroID)
        try:
            hero_id = query.filter(HeroModel.name == name).first()[0]
            return cls(hero_id)

        except TypeError:
            raise ValueError('Can not find id for hero name: {}'.format(name))

    # properties
    @property
    def str(self):
        return int(self.AttributeBaseStrength + \
                   (self.lvl - 1) * self.AttributeStrengthGain)

    @property
    def int(self):
        return int(self.AttributeBaseIntelligence + \
                   (self.lvl - 1) * self.AttributeAgilityGain)

    @property
    def agi(self):
        return int(self.AttributeBaseAgility + \
                   (self.lvl - 1) * self.AttributeAgilityGain)

    @property
    def health(self):
        return self.base_health + self.str * 20

    @property
    def health_regen(self):
        return self.base_health_regen + self.str * 0.03

    @property
    def mana(self):
        return self.int * 12

    @property
    def mana_regen(self):
        return self.int * 0.04

    @property
    def armor(self):
        return round(self.ArmorPhysical + self.agi / 7, 2)

    def has(self, effect):
        for ability, labels in self.abilities_labels().items():
            if effect in labels:
                return True

        return False

    def __str__(self):
        return '<Hero {name}, lvl={lvl}>'.format(name=self.name, lvl=self.lvl)


class Heroes(Group):

    member_type = Hero