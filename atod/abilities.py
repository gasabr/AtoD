import re
import json
import pandas

from atod import settings
from atod.tools.json2vectors import create_categorical, create_numeric
from atod.tools.dictionary import (find_all_values, create_encoding,
                                   make_flat_dict)

class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Abilities(metaclass=Singleton):
    ''' Singleton wrapper for npc_abilities.json.

        This class provides interface to work with abilities file.

        Attributes:
            _filename (str): absolute path to npc_abilities.json
            raw (dict)     : parsed npc_abilities.txt without any changes
    '''

    _filename = settings.ABILITIES_FILE

    def __init__(self):
        with open(self._filename, 'r') as fp:
            self.raw = json.load(fp)

    @property
    def skills(self):
        ''' Talents are not included. '''
        # load converter to get heroes names
        with open(settings.IN_GAME_CONVERTER, 'r') as fp:
            converter = json.load(fp)

        heroes_names = [c for c in converter.keys()
                        if re.findall(r'[a-zA-Z|\_]+', c)]

        # find all the heroes skills, but not talents
        skills_list = []
        for key, value in self.raw['DOTAAbilities'].items():
            # if ability contains hero name, doesn't contain special_bonus
            if any(map(lambda name: name in key, heroes_names)) and \
                            'special_bonus' not in key and \
                            'empty' not in key and \
                            'scepter' not in key:
                skills_list.append(key)

        skills = {}
        for ability in skills_list:
            skills[ability] = self.raw['DOTAAbilities'][ability]

        return skills

    @property
    def skills_list(self):
        return list(self.skills.keys())

    @property
    def skills_flat(self):
        skills_flat = {}
        for ability, description in self.skills.items():
            skills_flat[ability] = make_flat_dict(description)

        return skills_flat

    @property
    def effects(self):
        # FIXME: write better effects extraction here
        return set(e for effect in self.skills_flat for e in effect.split('_'))

    @property
    def encoding(self):
        '''Returns encoding of categorical features.'''
        values = find_all_values(self.raw['DOTAAbilities'])
        encoding = create_encoding(values)

        return encoding

    @property
    def frame(self):
        ''' Function to call from outside of the module.

            Returns:
                result_frame (pandas.DataFrame) : DataFrame of extracted vectors
        '''
        # cat stands for categorical
        cat_columns = ['{}={}'.format(k, vv) for k, v in self.encoding.items()
                       for vv in v if k != 'var_type' and
                       k != 'LinkedSpecialBonus' and
                       k != 'HotKeyOverride' and
                       k != 'levelkey']

        heroes_abilities = list(self.skills)
        skills = self.skills_flat

        numeric_part = create_numeric(skills, heroes_abilities, self.effects)
        categorical_part = create_categorical(skills,
                                              heroes_abilities,
                                              cat_columns)

        result_frame = pandas.concat([numeric_part, categorical_part], axis=1)

        return result_frame


abilities = Abilities()
