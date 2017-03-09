import re
import json
import pandas
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

from atod import settings
from atod.tools.json2vectors import create_categorical, create_numeric
from atod.tools.dictionary import (find_all_values, create_encoding,
                                   make_flat_dict)
from atod.ability import Ability

class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Abilities(metaclass=Singleton):
    ''' Singleton wrapper for npc_abilities.json.

        This class provides interface to work with abilities file.
        I'm using following definitions in the program:
            property    -- something that describes ability (e.g. cooldown)
            description -- all the properties of the ability
            skill       -- playable hero ability

        Attributes:
            _filename (str): absolute path to npc_abilities.json
            skills (dict)  : flatted skills from npc_abilities.json
    '''

    _filename = settings.ABILITIES_FILE

    def __init__(self):
        skills_raw = self.find_skills()

        self.skills = {}
        for ability, description in skills_raw.items():
            self.skills[ability] = make_flat_dict(description)

    def find_skills(self):
        with open(self._filename, 'r') as fp:
            raw = json.load(fp)

        # load converter to get heroes names
        with open(settings.IN_GAME_CONVERTER, 'r') as fp:
            converter = json.load(fp)

        heroes_names = [c for c in converter.keys()
                        if re.findall(r'[a-zA-Z|\_]+', c)]

        # find all the heroes skills, but not talents
        skills_list = []
        for key, value in raw['DOTAAbilities'].items():
            # if ability contains hero name, doesn't contain special_bonus
            if any(map(lambda name: name in key, heroes_names)) and \
                            'special_bonus' not in key and \
                            'empty' not in key and \
                            'scepter' not in key:
                skills_list.append(key)

        skills = {}
        for ability in skills_list:
            skills[ability] = raw['DOTAAbilities'][ability]

        return skills

    @property
    def raw(self):
        '''Returns npc_abilities.txt as a dict.'''
        with open(self._filename, 'r') as fp:
            return json.load(fp)

    @property
    def skills_list(self):
        return list(self.skills.keys())

    @property
    def effects(self):
        ''' Returns:
                (set): all words that occurs in abilities descriptions (keys)
        '''
        # FIXME: write better effects extraction
        return set(e for key, effects in self.skills.items()
                     for effect in effects
                     for e in effect.split('_'))

    @property
    def encoding(self):
        '''Returns encoding of categorical features.'''
        values = find_all_values(self.raw['DOTAAbilities'])
        encoding = create_encoding(values)

        return encoding

    @property
    def cat_columns(self):
        return ['{}={}'.format(k, vv) for k, v in self.encoding.items()
                       for vv in v if k != 'var_type' and
                       k != 'LinkedSpecialBonus' and
                       k != 'HotKeyOverride' and
                       k != 'levelkey']

    @property
    def frame(self):
        ''' Function to call from outside of the module.

            Returns:
                result_frame (pandas.DataFrame) : DataFrame of extracted vectors
        '''
        # cat stands for categorical

        heroes_abilities = list(self.skills)
        skills = self.skills

        numeric_part = create_numeric(skills, heroes_abilities, self.effects)
        categorical_part = create_categorical(skills,
                                              heroes_abilities,
                                              self.cat_columns)

        result_frame = pandas.concat([numeric_part, categorical_part], axis=1)

        return result_frame

    # TODO: merge this with filter() function
    def with_property(self, property_):
        ''' Finds properties which contain one of `keywords`.

            Args:
                property_ (list): property to look in ability description keys

            Returns:
                properties (dict): maps ability to its property value

        '''

        properties = []

        for ability, description in self.skills.items():
            # if ability has property - remember its value
            try:
                properties.append((ability, description[property_]))

            # otherwise - continue searching
            except KeyError:
                continue

        return properties

    def plot_property(self, property_):
        '''Plots all values of given property with matplotlib.

            Args:
                property_ (str): property to plot

        '''
        abilities_to_plot = self.with_property(property_)
        properties = pandas.Series([a[1] for a in abilities_to_plot],
                                   index=[a[0] for a in abilities_to_plot])

        # TODO: add borders to histogram
        # plotting
        # set styles
        sns.set(style="white", palette="muted", color_codes=True)
        sns.distplot(properties, color='b')
        plt.show()

    def clustering_by(self, property_):
        ''' Clusters abilities by given `property_`.

            Args:
                property_ (str): property to cluster by

            Returns:
                clusters (dict): maps skill to its cluster
        '''

        skills = self.with_property(property_)
        properties = [[a[1]] for a in skills]

        km = KMeans(n_clusters=3).fit(properties)

        # to get meaningful cluster name, map cluster center to word
        id2center = list()
        for cluster_i, cluster_center in enumerate(km.cluster_centers_):
            id2center.append((cluster_i, cluster_center[0]))

        id2center.sort(key=lambda c: c[1])

        # map id of cluster to the word describing its value
        id2label = dict()
        for label, value in zip([x[0] for x in id2center],
                                ['Small', 'Medium', 'Big']):
            id2label[label] = value

        # spread results to clusters
        clusters = {}
        for skill, cluster in zip([a[0] for a in skills], km.labels_):
            clusters[skill] = id2label[cluster] + property_

        return clusters

    def filter(self, hero=''):
        ''' Returns all the hero abilities.

            Plan is to add more filtering options, for example cooldown,
            effects(armor, slow, damage...).

            Args:
                hero (str): in game hero name
                    (optional, default='')

            Returns:
                abilities_ (list): list of Ability
        '''

        abilities_ = []
        if hero != '':
            for ability, description in self.skills.items():
                if hero in ability:
                    abilities_.append(Ability(ability, description))

        return abilities_

abilities = Abilities()