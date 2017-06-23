import pandas as pd

from atod import meta_info
from atod.db import session
from atod.models.interfaces import Group, Member
from atod.db_models.ability import AbilityModel
from atod.db_models.ability_specs import AbilitySpecsModel
from atod.db_models.ability_texts import AbilityTextsModel


class Ability(Member):
    ''' Representation of Ability data.

    Attributes:
        name (str): name of ability
        lvl (int) : level of ability

    '''

    model = AbilityModel

    def __init__(self, id_, lvl=0, patch=''):
        ''' Initializes Ability from id, lvl and patch. 
        
        Args:
            id_ (int): hero's id in the game, API responses store the same
            lvl (int, default=0): desired level of the hero
            patch (str, default=''): same as version of the game. Default 
                value means the latest available patch.
                
        Raises:
            In addition to Member._valid_arg_types() can raise
            ValueError: if there is no Ability with such ID 
        '''

        self._valid_arg_types(id_, lvl, patch)

        if lvl < 0 or lvl > 10:
            raise ValueError('Level should be in range [0, 10]')

        # check if user has set up model attribute
        if self.model is None:
            class_name = self.__class__.__name__
            raise ValueError('Please set up model for {}', format(class_name))

        # search row in model where id equal to id_
        if patch == '':
            current_patch = meta_info.patch
            res = session.query(self.model).filter(
                self.model.ID == id_,
                self.model.patch == current_patch).first()
        else:
            res = session.query(self.model).filter(
                self.model.ID == id_,
                self.model.patch == patch).first()

        if res is None:
            raise ValueError('There is no ability with id {}'.format(id_))

        # init super class
        super().__init__(res.ID)
        self.name = res.name
        self.lvl = lvl

    def _extract_properties(self, response):
        ''' Extracts properties from session response.

            Args:
                response (instance of the `model`): row in db
        '''

        bin_labels = response.__dict__.copy()

        bin_labels = {k: v for k, v in bin_labels.items()
                      if k != 'ID' and k != 'HeroID' and k != 'name'
                      and not k.startswith('_')}

        return bin_labels

    def __str__(self):
        return '<Ability name={}>'.format(self.name)

    def __repr__(self):
        return '<Ability object name={}>'.format(self.name)

    def get_description(self):
        ''' Combines specs and labels in one description. '''

        labels = self.get_labels()
        specs  = self.get_specs()

        # merge specs with labels
        series = pd.concat([specs, labels], axis=0)

        return series

    def get_labels(self):
        ''' Returns labels of ability. '''
        query = session.query(self.model)
        result = query.filter(self.model.ID == self.id).first()
        bin_labels = self._extract_properties(result)
        labels = pd.Series({'label_' + k: v for k, v in bin_labels.items()
                            if k != 'name' and k != 'HeroID'})
        labels['id'] = self.id
        labels['name'] = self.name

        return labels

    def get_specs(self, include=[]):
        ''' Returns specs of this ability.

        Args:
            include (list of strings, default=[]): columns that should be 
                included.

        Results:
            pd.DataFrame: data with fields from include for this ability.
            
        '''

        columns = [getattr(AbilitySpecsModel, col) for col in include]

        if columns:
            query = session.query(*columns)
        else:
            query = session.query(AbilitySpecsModel)

        if self.lvl == 0:
            # get stats for all lvls
            lvls = query.filter(AbilitySpecsModel.ID == self.id).all()
            # create DataFrame from lvls data
            try:
                all_specs = pd.DataFrame([p.__dict__ for p in lvls])
            except AttributeError:
                named_columns = [dict(zip(columns, p)) for p in lvls]
                all_specs = pd.DataFrame(named_columns)
            # split DataFrame to text and numbers columns
            # average numeric part
            num_part = all_specs.select_dtypes(exclude=[object]).mean()
            # take first row from text part (all rows are the same)
            str_part = all_specs.select_dtypes(include=[object]).loc[0]

            # merge parts together
            specs = pd.concat([str_part, num_part], axis=0)

        else:
            # get specs for defined lvl
            query = query.filter(AbilitySpecsModel.ID == self.id)
            lvl_specs = query.filter(AbilitySpecsModel.lvl == self.lvl)
            lvl_specs = lvl_specs.first()
            specs = pd.Series(lvl_specs.__dict__)

        if 'HeroID' in specs:
            specs = specs.drop(['HeroID'])

        return specs

    def get_texts(self):
        ''' Gets all the records in abilities_texts table for this ability.

            Returns:
                pd.Series: index contain columns of abilities_texts table.
                    Can be empty, if this ability is not represented in texts
                    table.
        '''

        query = session.query(AbilityTextsModel)
        texts_row = query.filter(AbilityTextsModel.id == self.id).first()

        if texts_row is None:
            return pd.Series([])
        else:
            return pd.Series(texts_row)


class Abilities(Group):

    member_type = Ability

    # TODO: write version with levels arguments
    @classmethod
    def from_hero_id(cls, HeroID, patch=''):
        ''' Adds to members all abilities of the hero with `HeroID`. '''
        response = session.query(AbilityModel.ID)
        response = response.filter(AbilityModel.HeroID == HeroID).all()

        if len(response) == 0:
            report = 'No abilities for this HeroID == {}'.format(HeroID)
            raise ValueError(report)

        members_ = [cls.member_type(a[0], patch=patch) for a in response]

        return cls(members_)

    # TODO: this can be generalized with `member_type.model.ID`
    @classmethod
    def all(cls):
        ''' Creates Abilities object with all heroes abilities in the game.'''
        ids = [x[0] for x in session.query(AbilityModel.ID).all()]
        # XXX: would be nice to create members only if they are needed
        members_ = [Ability(id_) for id_ in ids]

        return cls(members_)

    def get_list(self):
        ''' Returns information about members in the form: row is a member.

            'List' because descriptions are just concatenated with each other,
            but not summed by any means.

            Returns:
                pd.DataFrame: shape=(len(self.members),
                    len(<member description>)). Rows are abilities, columns -
                    their properties. Labels columns names start with
                    'label_'.
        '''

        # get all descriptions
        descriptions = [m.get_description() for m in self.members]

        return pd.DataFrame(descriptions, columns=descriptions[0].index,
                            index=None)

    def get_specs_list(self, include=[]):
        ''' Returns list of all member's descriptions (ONLY specs part).

            Returns:
                pd.DataFrame: shape=(len(members), len(<member description>)).
                    Rows are abilities, columns - their properties.
                    Labels columns names start with 'label_'.
        '''

        # get all descriptions
        descriptions = [m.get_specs(include) for m in self.members]

        return pd.DataFrame(descriptions, columns=descriptions[0].index,
                            index=None)

    def get_labels_list(self):
        ''' Returns list of all member's descriptions (ONLY specs part).

            Returns:
                pd.DataFrame: shape=(len(members), len(<member description>)).
                    Rows are abilities, columns - their properties.
                    Labels columns names start with 'label_'.
        '''

        # get all descriptions
        descriptions = [m.get_labels() for m in self.members]

        return pd.DataFrame(descriptions, columns=descriptions[0].index)

    def get_texts(self):
        ''' Returns:
                pd.DataFrame: texts of abilities in DataFrame.
        '''

        # get members ids
        members_ids = [m.id for m in self.members]
        # get all texts
        all_texts = session.query(AbilityTextsModel).all()
        # find texts for members by ids
        members_texts = [row for row in all_texts
                         if any(map(lambda x: row.ID == x, members_ids))]

        # create DataFrame from chosen rows
        texts = pd.DataFrame([m.__dict__ for m in members_texts])
        texts = texts.drop(['_sa_instance_state'], axis=1)

        return texts

    def get_summary(self):
        ''' Sums up all labels of members (they are binary decoded).

            Returns:
                pd.Series:
        '''

        labels_list = self.get_labels_list()
        summary = labels_list.sum(axis=0)
        del summary['name']

        return summary
