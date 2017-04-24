''' This module describes single hero ability.'''
import pandas as pd

from atod.db import session
from atod.interfaces import Group, Member
from atod.models.ability import AbilityModel
from atod.models.ability_specs import AbilitySpecsModel


class Ability(Member):
    '''Wrapper around Abilities data.'''

    model = AbilityModel

    def __init__(self, id_, lvl=0):
        # check if user has set up model attribute
        if self.model is None:
            class_name = self.__class__.__name__
            raise ValueError('Please set up model for {}', format(class_name))

        # search row in model where id equal to id_
        res = session.query(self.model).filter(self.model.ID == id_).first()

        # init super class
        super().__init__(res.ID, res.name)
        self.lvl = lvl

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
        return '<Ability name={}>'.format(self.name)

    def __repr__(self):
        return '<Ability object name={}>'.format(self.name)

    def to_series(self):
        request = session.query(AbilitySpecsModel)
        if self.lvl == 0:
            # get stats for all lvls
            lvls = request.filter(AbilitySpecsModel.ID == self.id).all()
            # create DataFrame from lvls data
            all_specs = pd.DataFrame([p.__dict__ for p in lvls])
            # split DataFrame to text and numbers columns
            # average numeric part
            num_part = all_specs.select_dtypes(exclude=[object]).mean()
            # take first row from text part (all rows are the same)
            str_part = all_specs.select_dtypes(include=[object]).loc[0]

            # merge parts together
            specs = pd.concat([str_part, num_part], axis=0)

        else:
            # get specs for defined lvl
            request = request.filter(AbilitySpecsModel.ID == self.id)
            lvl_specs = request.filter(AbilitySpecsModel.lvl == self.lvl)
            lvl_specs = lvl_specs.first()
            specs = pd.Series(lvl_specs.__dict__)

        specs = specs.drop(['HeroID'])

        query = session.query(self.model)
        result = query.filter(self.model.ID == self.id).first()
        bin_labels = self._extract_properties(result)
        labels = {'label_' + k: v for k, v in bin_labels.items()}

        # merge specs with labels
        series = pd.concat([specs, pd.Series(labels)], axis=0)

        return series


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

    @classmethod
    def all(cls):
        ids = [x[0] for x in session.query(AbilityModel.ID).all()]
        members_ = [Ability(id_) for id_ in ids]

        return cls(members_)

    def get_labels_summary(self):
        bin_vectors = [m.bin_labels for m in self.members]

        # FIXME: can't make it work other way
        summary = bin_vectors[0]
        for b in bin_vectors[1:]:
            summary = summary + b

        del summary['name']

        return summary
