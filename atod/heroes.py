import pandas as pd
from sqlalchemy.inspection import inspect

from atod.db import session
from atod.models.hero import HeroModel
from atod.abilities import Abilities
from atod.interfaces import Group, Member

mapper = inspect(HeroModel)

PRIMARIES = {
    'DOTA_ATTRIBUTE_AGILITY': 'agility',
    'DOTA_ATTRIBUTE_STRENGTH': 'strength',
    'DOTA_ATTRIBUTE_INTELLECT': 'intellect',
}

laning_keys = [
    'RequiresFarm',
    'RequiresSetup',
    'RequiresBabysit',
    'ProvidesSetup',
    'SoloDesire',
    'SurvivalRating',
    'ProvidesBabysit'
]

all_roles = ['Disabler', 'Nuker', 'Escape', 'Durable', 'Initiator', 'Pusher',
         'Support', 'Jungler', 'Carry']

all_heroes_types = ['DOTA_BOT_PUSH_SUPPORT', 'DOTA_BOT_STUN_SUPPORT',
                    'DOTA_BOT_SEMI_CARRY', 'DOTA_BOT_HARD_CARRY',
                    'DOTA_BOT_NUKER', 'DOTA_BOT_TANK',
                    'DOTA_BOT_PURE_SUPPORT', 'DOTA_BOT_GANKER']

class Hero(Member):
    ''' Interface for HeroModel. '''

    base_health = 200
    base_health_regen = 0.25
    base_mana = 50
    base_mana_regen = 0.01
    base_damage = 21
    base_armor = -1

    def __init__(self, id_, lvl=1):
        query = session.query(HeroModel)
        specs = query.filter(HeroModel.HeroID == id_).first()
        super().__init__(specs.HeroID, specs.name)

        self.in_game_name = specs.in_game_name
        del specs.__dict__['name']
        # remove SQLAlchemy condition variable
        del specs.__dict__['_sa_instance_state']

        self.lvl = lvl
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

    def get_description(self):
        return pd.Series({'name': self.name, **self.specs,
                          **self.abilities.get_summary()})

    # properties
    @property
    def str(self):
        return int(self.specs['AttributeBaseStrength'] + \
                   (self.lvl - 1) * self.specs['AttributeStrengthGain'])

    @property
    def int(self):
        return int(self.specs['AttributeBaseIntelligence'] + \
                   (self.lvl - 1) * self.specs['AttributeAgilityGain'])

    @property
    def agi(self):
        return int(self.specs['AttributeBaseAgility'] + \
                   (self.lvl - 1) * self.specs['AttributeAgilityGain'])

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
        return round(self.specs['ArmorPhysical'] + self.agi / 7, 2)

    def __str__(self):
        return '<Hero {name}, lvl={lvl}>'.format(name=self.name, lvl=self.lvl)

    def get_laning_info(self):
        ''' Returns:
                pd.Series: laning info of this hero.
                
            Notes:
                The latest heroes does not have this field, so Series filled
                with zeroes would be returned.
        '''
        return pd.Series({k: self.specs[k] for k in laning_keys})

    def get_roles(self):
        ''' Returns:
                pd.Series: roles levels of this hero.
                
            Notes:
                The latest heroes does not have this field, so Series filled
                with zeroes would be returned.
        '''

        # map string roles stored in string to levels stored also in string
        roles = {role: lvl for role, lvl in
                 zip(self.specs['Role'].split(','),
                     self.specs['Rolelevels'].split(','))}

        roles = pd.Series(roles, index=all_roles)
        roles = roles.fillna(0)

        return roles

    def get_hero_type(self):
        ''' Returns:
                pd.Series: laning info of this hero.
                
            Notes:
                The latest heroes does not have this field, so Series filled
                with zeroes would be returned.
        '''

        types = dict()
        type_prefix = 'dota_bot_'
        for type_ in all_heroes_types:
            # change in game format to more readable
            clean_type = type_[len(type_prefix):].lower()
            # if hero belongs to that type
            if type_ in self.specs['HeroType']:
                types[clean_type] = 1
            else:
                types[clean_type] = 0

        return pd.Series(types)


class Heroes(Group):

    member_type = Hero

    # TODO: encode role and laning info
    def get_summary(self):
        ''' Sums up numeric properties, encodes and sums up categorical. '''
        # encode role
        # encode laning info
        # concatenate all the information together
        # sum up
        pass
