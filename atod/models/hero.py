import re
import pandas as pd
from sqlalchemy import inspect
from sqlalchemy.orm import scoped_session, sessionmaker

from atod import Member, meta_info, Abilities
from atod.db import engine
from atod.db_models.hero import HeroModel

session = scoped_session(sessionmaker(bind=engine))


class Hero(Member):
    ''' Representation of single Hero.

    Attributes:
        name (str)           : name of the hero
        in_game_name (str)   : name that is used for hero inside the game
        lvl (int)            : current hero lvl
        specs (dict)         : raw db row as dictionary
        abilities (Abilities): representation of hero's abilities

    '''

    model = HeroModel

    # FIXME: This info should be read from file/db not hardcoded
    base_health = 200
    base_health_regen = 0.25
    base_mana = 50
    base_mana_regen = 0.01
    base_damage = 21
    base_armor = -1

    def __init__(self, id_: int, lvl=1, patch=''):
        ''' Initializes Hero by default with level one from the last patch.

        Args:
            id_ (int): hero's id in the game, API responses store the same
            lvl (int): desired level of the hero
            patch (str): same as version of the game
            name (str) : hero's name
            in_game_name(str): in-game hero's name (used in game console)

        Raises:
            see Member._valid_arg_types() for info.
        '''

        # raise an exception if types are incorrect
        self._valid_arg_types(id_, lvl, patch)

        query = session.query(self.model)

        if patch == '':
            current_patch = meta_info.patch
            specs = query.filter(self.model.HeroID == id_,
                                 self.model.patch == current_patch).first()
        else:
            specs = query.filter(self.model.HeroID == id_,
                                 self.model.patch == patch).first()

        if specs is None:
            raise ValueError('No hero with id {}'.format(id_))

        super().__init__(specs.HeroID, lvl, patch)

        self.name = specs.name
        self.in_game_name = specs.in_game_name

        # remove SQLAlchemy condition variable
        del specs.__dict__['_sa_instance_state']

        self.lvl = lvl
        self.specs = specs.__dict__
        try:
            self.abilities = Abilities.from_hero_id(self.id, patch)
        except ValueError:
            print('Known bug: hero with id '
                  '{} does not have abilities in db.'.format(self.id))

    @classmethod
    def from_name(cls, name, lvl=1, patch=''):
        ''' Converts name to id with and calls init.

        Args:
            name (str) : hero's is game name in the game
            lvl (int)  : desired level of the hero
            patch (str): same as version of the game

        Raises:
            ValueError: if `name` is not in heroes.name column
            TypeError : if `name` is not str
            Also can raise same as __init__() for the same reasons.
        '''

        # valid name, everything else will be checked in init function
        if not isinstance(name, str):
            raise TypeError('Name should be `str`,'
                            'got {} instead'.format(type(name)))

        query = session.query(HeroModel.HeroID)
        try:
            hero_id_ = query.filter(cls.model.name == name).first()
            # try to search hero for in_game_name if the name aws not found
            if hero_id_ is None:
                hero_id_ = query.filter(cls.model.in_game_name == name).first()
            
            hero_id = hero_id_[0] 

            return cls(hero_id, lvl, patch)

        except TypeError:
            raise ValueError('Can not find id for hero name: {}'.format(name))

    def get_description(self, include: list):
        ''' Constructs hero description.

        Possible include values:
        * 'name'
        * 'id'
        * 'laning'
        * 'role'
        * 'type'
        * 'attributes'

        Args:
            include (list, default=[]): tells how the hero should be described.

        '''

        if not isinstance(include, list):
            raise TypeError('`include` should be list.')

        description = list()

        for field in include:
            if field == 'name':
                description.append(pd.Series({'name': self.name}))
            elif field == 'id':
                description.append(pd.Series({'id': self.id}))
            elif field == 'laning':
                description.append(self._get_laning())
            elif field == 'role':
                description.append(self._get_role())
            elif field == 'type':
                description.append(self._get_type())
            elif field == 'attributes':
                description.append(self._get_attributes())
            else:
                print('{} is not one of possible descriptions.'.format(field))

        if len(description) == 0:
            raise ValueError('include argument should contain at least'
                             'one of the ["name", "id", "laning", '
                             '"roles", "type", "attributes"]')

        return pd.concat(description)

    # properties
    @property
    def primary_attribute(self):
        ''' Returns primary attribute as string in lower case. '''
        primaries = session.query(HeroModel.AttributePrimary)
        hero_primary = primaries.filter(HeroModel.HeroID == self.id).first()[0]

        prefix = 'DOTA_ATTRIBUTE_'
        hero_primary = hero_primary[len(prefix):].lower()

        return hero_primary

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

    def _get_laning(self):
        ''' Returns:
                pd.Series: laning info of this hero.

            Notes:
                The latest heroes does not have this field, so Series filled
                with zeroes would be returned.
        '''
        laning_info = dict()
        multi_index_keys = list()

        for key in laning_keys:
            multi_index_keys.append(camel2python(key))
            laning_info[camel2python(key)] = self.specs[key]

        multi_index = [['laning'] * len(laning_keys),
                        multi_index_keys]

        laning_info = pd.Series(laning_info, index=multi_index)

        print(type(laning_info.index))

        return laning_info

    def _get_role(self):
        ''' Returns:
                pd.Series: role levels of this hero.

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

    def _get_type(self):
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

    def _get_primary_attribute(self):
        prefix = 'DOTA_'
        encoded = dict()

        for k in primaries:
            clean_key = 'primary_' + k[len(prefix):].lower()
            encoded[clean_key] = 1 if self.specs['AttributePrimary'] == k else 0

        encoded = pd.Series(encoded)
        encoded = encoded.fillna(value=0)

        return encoded

    def _get_attributes(self):
        ''' Returns only attributes which are not encoded. '''
        attributes = {camel2python(k): self.specs[k] for k in attributes_list}
        attributes = pd.Series(attributes).fillna(value=0)

        return attributes


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
