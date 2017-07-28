import pandas as pd
from sqlalchemy.orm import sessionmaker, scoped_session

from atod import Member, meta_info
from atod.db import engine
from atod.db_models.ability import AbilityModel
from atod.db_models.ability_specs import AbilitySpecsModel
from atod.db_models.ability_texts import AbilityTextsModel

session = scoped_session(sessionmaker(bind=engine))


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

        # check if model attrubute is set up
        if self.model is None:
            class_name = self.__class__.__name__
            raise ValueError('Please set up model for {}', format(class_name))

        # get information from the database if patch is not specified
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
        super().__init__(res.ID, lvl, patch)
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

    def get_description(self, include: list):
        ''' Combines specs and labels in one description.

        Possible values in `include` list:
            * labels
            * specs
            * texts
            * name
            * id

        Args:
            include: list of fields which should be included in description.

        Returns:
            pd.DataFrame: description with requested fields.

        '''

        descriptions = list()

        for field in include:
            if field == 'labels':
                descriptions.append(self._get_labels())
            elif field == 'specs':
                descriptions.append(self._get_specs())
            elif field == 'texts':
                descriptions.append(self._get_texts())
            elif field == 'name':
                descriptions.append(pd.Series([self.name]))
            elif field == 'id':
                descriptions.append(pd.Series([self.id]))
            else:
                print('{} is not one of possible descriptions.'.format(field))

        # merge all descriptions
        series = pd.concat(descriptions, axis=0)

        return series

    def _get_labels(self):
        ''' Returns labels of ability. '''
        query = session.query(self.model)
        result = query.filter(self.model.ID == self.id).first()
        bin_labels = self._extract_properties(result)
        labels = pd.Series({'label_' + k: v for k, v in bin_labels.items()
                            if k != 'name' and k != 'HeroID'
                            and k != 'patch' and k != 'index'})

        return labels

    def _get_specs(self):
        ''' Returns specs of this ability.

        Results:
            pd.DataFrame: data with fields from include for this ability.

        '''

        query = session.query(AbilitySpecsModel)

        if self.lvl == 0:
            # get stats for all lvls
            lvls = query.filter(AbilitySpecsModel.ID == self.id).all()
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
            query = query.filter(AbilitySpecsModel.ID == self.id)

            lvl_specs = query.filter(AbilitySpecsModel.lvl == self.lvl)
            lvl_specs = lvl_specs.first()

            specs = pd.Series(lvl_specs.__dict__)

        if 'HeroID' in specs:
            specs = specs.drop(['HeroID', 'patch', 'index'])

        return specs

    def _get_texts(self):
        ''' Gets all the records in abilities_texts table for this ability.

            Returns:
                pd.Series: containing id, description, lore, name, notes and
                    others fields. Will be completely empty, if this ability
                    is not represented in texts table.
        '''

        query = session.query(AbilityTextsModel)
        texts_row = query.filter(AbilityTextsModel.ID == self.id).first()

        if texts_row is None:
            return pd.Series([])
        else:
            result = pd.Series(texts_row.__dict__)
            result = result.drop(['_sa_instance_state'])

            return result
