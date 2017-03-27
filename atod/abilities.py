import json
import re

import matplotlib.pyplot as plt
import pandas
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import MultiLabelBinarizer, MinMaxScaler

from atod import settings
from atod.ability import Ability
from atod.utils.preprocessing.abilities import (create_categorical,
                                    encode_effects, fill_numeric)
from atod.utils.dictionary import (find_all_values, create_encoding,
                                   make_flat_dict)
from atod.utils.preprocessing.clean_abilities import clean as cleaning_function
from atod.utils.preprocessing.load_labels import load_labels


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

    unused_properties = ['HasScepterUpgrade', 'LinkedSpecialBonus',
                         'HotKeyOverride', 'levelkey', 'FightRecapLevel',
                         'CalculateSpellDamageTooltip']

    def __init__(self):
        self.clean = cleaning_function()
        self.skills = dict()
        for ability, description in self.clean.items():
            self.skills[ability] = description

        self.cat_variables = self.get_cat_variables()

        self.cat_columns = ['{}={}'.format(k, vv)
                            for k, v in self.encoding.items()
                            for vv in v if k in self.cat_variables]

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
    def specials(self):
        '''Returns mapping ability -> AbilitySpecials without excluded.'''
        excluded = ['CalculateSpellDamageTooltip',
                    'LinkedSpecialBonusOperation', 'LinkedSpecialBonus']

        specials = dict()
        raw = self.raw['DOTAAbilities']
        # TODO: extend function to more common case (with property())
        key = 'AbilitySpecial'
        for ability, description in raw.items():
            if ability not in self.skills.keys():
                continue

            try:
                specials[ability] = make_flat_dict(description[key],
                                                   exclude=excluded)
            except KeyError:
                pass
            # to handle Version
            except TypeError:
                pass


        return specials

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

    def get_properties(self):
        return set(effect for key, effects in self.skills.items()
                          for effect in effects
                          if effect not in self.unused_properties)

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

        clean = self.clean_properties()
        heroes_abilities = list(clean)
        skills = clean

        numeric_part = encode_effects(skills, heroes_abilities, self.effects)
        categorical_part = create_categorical(skills,
                                              heroes_abilities,
                                              self.cat_columns)

        result_frame = pandas.concat([numeric_part, categorical_part], axis=1)

        return result_frame

    @property
    def clean_frame(self):
        ''' Function to call from outside of the module.

            Returns:
                result_frame (pandas.DataFrame) : DataFrame of extracted vectors
        '''

        # clean = self.clean_properties()
        clean = cleaning_function()
        heroes_abilities = list(clean)

        effects = [effect for key, effects in clean.items()
                          for effect in effects
                          if effect not in self.unused_properties]

        effects = set(effects)

        # fill categorical variables
        categorical_part = create_categorical(clean,
                                              heroes_abilities,
                                              self.cat_columns)

        # remove categorical variables from description
        for skill, description in clean.items():
            for cat in self.cat_variables:
                if cat in description:
                    del description[cat]

        # fill numeric part of dataframe
        numeric_part = fill_numeric(clean, heroes_abilities, effects)

        # concatenate 2 parts
        result_frame = pandas.concat([numeric_part, categorical_part], axis=1)
        # result_frame = result_frame.drop(['changed', 'ID'], axis=1)
        # result_frame = result_frame.dropna(axis=1, thresh=2)
        # result_frame = result_frame.fillna(value=0)

        return result_frame

    @property
    def effects_descriptions(self):
        ''' Generator of not categorical properties strings.

            Yields:
                property_ (str): property where '_' replaced with ' '
        '''
        print(self.cat_variables)
        for skill, description in self.skills.items():
            for property_ in description:
                if property_ not in self.cat_variables:
                    yield property_.replace('_', ' ')

    def get_cat_variables(self):
        return set([k for k, v in self.encoding.items()
                      for vv in v if k != 'var_type' and
                                     k != 'LinkedSpecialBonus' and
                                     k != 'HotKeyOverride' and
                                     k != 'levelkey'])

    # TODO: merge this with filter() function
    def with_property(self, property_):
        ''' Finds properties which contain one of `keywords`.

            Args:
                property_ (str): property to look in ability description keys

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
        ''' Plots all values of given property with matplotlib.

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

    def clean_properties(self):
        ''' Removes parts of ability name from all the properties.

            There are a lot of skills which properties looks like this:
            <skillname>_<property>, they could be simplified to <property>.
            This function does exactly that.

            Returns:
                clean (dict): cleaned skills dictionary, where every changed
                    ability has special keyword `changed`.
        '''
        clean = self.skills.copy()
        for skill, description in clean.items():
            skill_changed = False
            for property_ in list(description):
                property_split = property_.split('_')
                new_name_list = [p for p in property_split if p not in skill]

                if new_name_list != property_split and len(new_name_list) != 0:
                    new_name = ''.join([n + '_' for n in new_name_list]).strip('_')
                    clean[skill][new_name] = description[property_]
                    del clean[skill][property_]
                    skill_changed = True

                else:
                    continue

            if skill_changed:
                clean[skill]['changed'] = True

        return clean

    def load_train_test(self):
        ''' Loads training and test data for classification.

            Returns:
                X_train, y_train, X_test  of pd.DataFrame)
        '''

        frame = self.clean_frame
        labeling = load_labels()
        labeled_abilities = list(labeling)
        # list of labels as integers
        labels_unique = [labeling[a] for a in labeled_abilities]

        # binarize data
        mlb = MultiLabelBinarizer()
        labels_bin = mlb.fit_transform(labels_unique)

        labels = pandas.DataFrame(labels_bin, index=labeled_abilities,
                                  columns=settings.LABELS)

        mm_scaler = MinMaxScaler()
        mm_scaler.fit(frame)

        # get labeled skill from frame
        train = frame.loc[list(labeling)]
        train = train.fillna(value=0)
        train = mm_scaler.transform(train)

        # drop labeled skill from frame
        frame = frame.drop([a for a in labeling if a in frame.index], axis=0)
        # frame = mm_scaler.transform(frame)

        return train, labels, frame

abilities = Abilities()