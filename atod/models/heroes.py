import re
import pandas as pd
from sqlalchemy.inspection import inspect

from atod.db import session
from atod.db_models.hero import HeroModel
from atod.models.abilities import Abilities
from atod.models.interfaces import Group, Member

mapper = inspect(HeroModel)

attributes_list = [
    'ArmorPhysical',
    'AttackAcquisitionRange',
    'AttackAnimationPoint',
    'AttackDamageMax',
    'AttackDamageMin',
    'AttackRange',
    'AttackRate',
    'AttributeAgilityGain',
    'AttributeBaseAgility',
    'AttributeBaseIntelligence',
    'AttributeBaseStrength',
    'AttributeIntelligenceGain',
    'AttributeStrengthGain',
    'MovementSpeed',
    'MovementTurnRate',
 ]

primaries = {
    'DOTA_ATTRIBUTE_AGILITY', 'DOTA_ATTRIBUTE_STRENGTH',
    'DOTA_ATTRIBUTE_INTELLECT',
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


# TODO: move this function to mo appropriate place
def camel2python(inp):
    ''' Converts camel style string to lower case with unders.

        Args:
            inp (string): string to be converted

        Returns:
            string: result
    '''

    # split string into pieces started with capital letter
    words = re.findall(r'[A-Z][a-z]+', inp)
    result = '_'.join([word.lower() for word in words])

    return result


class Hero(Member):
    ''' Interface for HeroModel. '''

    model = HeroModel

    base_health = 200
    base_health_regen = 0.25
    base_mana = 50
    base_mana_regen = 0.01
    base_damage = 21
    base_armor = -1

    def __init__(self, id_, lvl=1):
        query = session.query(self.model)
        specs = query.filter(self.model.HeroID == id_).first()
        super().__init__(specs.HeroID)

        self.name = specs.name
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
            hero_id = query.filter(cls.model.name == name).first()[0]
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
        laning_info = dict()
        for key in laning_keys:
            laning_info['laning_' + camel2python(key)] = self.specs[key]

        laning_info = pd.Series(laning_info).fillna(value=0)

        return laning_info

    def get_roles(self):
        ''' Returns:
                pd.Series: roles levels of this hero.

            Notes:
                The latest heroes does not have this field, so Series filled
                with zeroes would be returned.
        '''

        # map string roles stored in string to levels stored also in string
        if len(self.specs['Rolelevels'].split(',')) == 0:
            print('{} does not have roles.'.format(self.name))

        roles = dict()
        for role, lvl in zip(self.specs['Role'].split(','),
                             self.specs['Rolelevels'].split(',')):
            key = 'role_' + role.lower()
            value = int(lvl)

            roles[key] = value

        roles = pd.Series(roles,
                          index=map(lambda x: 'role_' + x.lower(), all_roles))
        roles = roles.fillna(0)

        return roles

    def get_hero_type(self):
        ''' Returns:
                pd.Series: binary encoded type of this hero.

            Notes:
                The latest heroes does not have this field, so Series filled
                with zeroes would be returned.
        '''

        types = dict()
        type_prefix = 'dota_bot_'
        for type_ in all_heroes_types:
            # change in game format to more readable
            clean_type = 'type_' + type_[len(type_prefix):].lower()
            # if hero belongs to that type
            if self.specs['HeroType'] is not None \
                        and type_ in self.specs['HeroType']:
                types[clean_type] = 1
            else:
                types[clean_type] = 0

        types = pd.Series(types).fillna(value=0)

        return types

    def get_primary_attribute(self):
        prefix = 'DOTA_'
        encoded = dict()

        for k in primaries:
            clean_key = 'primary_' + k[len(prefix):].lower()
            encoded[clean_key] = 1 if self.specs['AttributePrimary'] == k else 0

        encoded = pd.Series(encoded)
        encoded = encoded.fillna(value=0)

        return encoded

    def get_attributes(self):
        ''' Returns only attributes which are not encoded. '''
        attributes = {camel2python(k): self.specs[k] for k in attributes_list}
        attributes = pd.Series(attributes).fillna(value=0)

        return attributes

    def get_bin_description(self):
        ''' Returns description with all the variables encoded. '''
        description = [self.get_attributes(), self.get_roles(),
                       self.get_primary_attribute(), self.get_hero_type(),
                       self.get_laning_info(), pd.Series({'name': self.name}),
                       self.abilities.get_summary()]

        return pd.concat(description)

class Heroes(Group):

    member_type = Hero

    @classmethod
    def from_ids(cls, ids):
        member_model = cls.member_type.model

        members_ = list()
        for id_ in ids:
            try:
                members_.append(cls.member_type(id_))
            # XXX: can not create abilities for hero with HeroID == 16
            except ValueError as e:
                print(e)

        return cls(members_)

    @classmethod
    def all(cls):
        ''' Creates Abilities object with all heroes abilities in the game.'''
        member_model = cls.member_type.model
        ids = [x[0] for x in session.query(member_model.HeroID).all()]

        members_ = list()
        for id_ in ids:
            try:
                members_.append(cls.member_type(id_))
            # XXX: can not create abilities for hero with HeroID == 16
            except ValueError as e:
                print(e)

        return cls(members_)

    def get_summary(self):
        ''' Sums up numeric properties, encodes and sums up categorical. '''
        descriptions = [m.get_bin_description() for m in self.members]
        descriptions = pd.DataFrame(descriptions)

        # no use to the name in summary
        descriptions = descriptions.drop(['name', 'id'], axis=1)
        columns_summary = [sum(descriptions[c]) for c in descriptions.columns]
        summary = pd.Series(columns_summary, index=descriptions.columns)

        return summary

    def get_names(self):
        return [m.name for m in self.members]
