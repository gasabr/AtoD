''' This module describes single hero ability.'''
import pandas as pd

from atod.db import session
from atod.interfaces import Group, Member
from atod.models import AbilityModel, AbilitySpecsModel


class Ability(Member):
    '''Wrapper around Abilities data.'''

    model = AbilityModel

    def __init__(self, id_):
        # check if user has set up model attribute
        if self.model is None:
            class_name = self.__class__.__name__
            raise ValueError('Please set up model for {}', format(class_name))

        # search row in model where id equal to id_
        res = session.query(self.model).filter(self.model.ID == id_).first()

        # init super class
        super().__init__(res.ID, res.name)
        # define default lvl
        self.lvl = 0

        self._bin_labels = self._extract_properties(res)
        self._labels = [l for l in self._bin_labels
                        if self._bin_labels[l] == 1]

        # get specs IMPORTANT: ID is not pk for this table, abilities are
        # stored by level, so every ability has at least 3 records
        specs = session.query(AbilitySpecsModel)
        lvls  = specs.filter(AbilitySpecsModel.ID == id_).all()

        # add specs as dictionaries
        self.all_specs = dict()
        self.specs = dict()
        for record in lvls:
            lvl = record.lvl
            self.all_specs[lvl] = self._extract_properties(record)
            self.specs[lvl] = {k: v for k, v in self.all_specs[lvl].items()
                               if v is not None}

    def _extract_properties(self, response):
        ''' Extracts properties from session response. 
        
            Args:
                response (instance of the `model`): row in db
        '''

        bin_labels = response.__dict__.copy()

        bin_labels = {k: v for k, v in bin_labels.items()
                      if k != 'ID' and k != 'HeroID'
                      and not k.startswith('_')}

        return bin_labels

    def __str__(self):
        return '<Ability name={}, labels={}>'.format(self.name, self._labels)

    def __repr__(self):
        return '<Ability object name={}>'.format(self.name)

    @property
    def bin_labels(self):
        ''' Returns vector representation of this ability.
        
            Returns:
                vector (pd.Series): vector build upon all_labels attribute
        '''
        return pd.Series(self._bin_labels)

    def to_series(self):
        if self.lvl == 0:
            # average all specs
            summary = self._get_summary()

        else:
            # get specs for defined lvl
            summary = self.all_specs[self.lvl]

        summary['id'] = self.id
        labels = {'label_' + k: v for k, v in self._bin_labels.items()}

        # merge specs with labels
        series = pd.concat([summary, pd.Series(labels)], axis=0)

        return series

    def _get_summary(self):
        ''' Return series where every features are averaged. 
        
            This function averages all the properties.
             
             Returns:
                 summary (pd.Series): described summary
        '''
        summary = pd.Series(self.specs[1])
        sum_dict = dict()
        for lvl in range(1, len(self.specs)):
            for prop, value in self.specs[lvl].items():
                if isinstance(value, int) or isinstance(value, float):
                    sum_dict.setdefault(prop, 0)
                    sum_dict[prop] += value / len(self.specs)

        for column in self.all_specs[1]:
            if column not in summary:
                summary[column] = None

        summary = summary.drop('pk')

        return summary


class Abilities(Group):

    member_type = Ability

    @classmethod
    def from_hero_id(cls, HeroID):
        response = session.query(AbilityModel.ID)
        response = response.filter(AbilityModel.HeroID == HeroID).all()

        if len(response) == 0:
            report = 'No abilities for this HeroID == {}'.format(HeroID)
            raise ValueError(report)

        members_ = [cls.member_type(ability[0]) for ability in response]

        return cls(members_)

    def get_labels_summary(self):
        bin_vectors = [m.bin_labels for m in self.members]

        # FIXME: can't make it work other way
        summary = bin_vectors[0]
        for b in bin_vectors[1:]:
            summary = summary + b

        del summary['name']

        return summary
