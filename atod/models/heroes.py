import pandas as pd
from sqlalchemy.orm import sessionmaker, scoped_session

from atod import Hero
from atod.db import engine
from atod.db_models.hero import HeroModel
from atod.models.interfaces import Group

session = scoped_session(sessionmaker(bind=engine))


class Heroes(Group):

    member_type = Hero

    @classmethod
    def from_ids(cls, ids: list, patch=''):
        ''' Creates Heroes object from list of ids. '''
        members_ = list()
        for id_ in ids:
            members_.append(cls.member_type(id_, patch=patch))

        return cls(members_)

    @classmethod
    def from_names(cls, names: list, patch=''):
        ''' Creates Heroes object from list of names. '''
        members_ = list()
        for name in names:
            members_.append(Hero.from_name(name, patch=patch))

        return cls(members_)

    @classmethod
    def all(cls, patch=''):
        ''' Creates Heroes object with all heroes in the game.'''
        member_model = cls.member_type.model
        ids = [x[0] for x in session.query(member_model.HeroID).all()]

        members_ = list()
        for id_ in ids:
            members_.append(cls.member_type(id_, patch=patch))

        return cls(members_)

    def get_description(include):
        ''' Sums up heroes descriptions in included categories.

        Notes:
            'name' and 'id' will be dropped because where is no reason to
            add together string and hero id.

        Returns:
            pd.Series: sum of desired attributes for all members (heroes).

        '''

        descriptions_ = [m.get_description(include) for m in self.members]
        descriptions = pd.DataFrame(descriptions_)

        # no use to the name in summary
        if 'name' in descriptions.columns:
            descriptions = descriptions.drop(['name'], axis=1)
        if 'id' in descriptions.columns:
            descriptions = descriptions.drop(['id'], axis=1)

        columns_summary = [sum(descriptions[c]) for c in descriptions.columns]
        summary = pd.Series(columns_summary, index=descriptions.columns)

        return summary

    def get_names(self):
        ''' Returns:
                list: names of members.
        '''
        return [m.name for m in self.members]

    def get_ids(self, binarised=False):
        ''' Returns heroes ids.

        Can be useful, when you have a team and instead of getting id for all
        heroes you use this.

        Args:
            binarised (bool, default=False): if bin the function will return
                binarised vector of heroes ids, so you don't need to know how
                many heroes are in the game.

        Returns:
            pd.Series: shape=(, len(self.members)) by default, if binary version
                was requested shape=(, # heroes in the game).

        '''

        name2id = {m.name: m.id  for m in self.members}

        if binarised:
            all_ids = [h[0] for h in session.query(HeroModel.HeroID).all()]
            members_ids = [id_ for id_ in name2id.values()]
            bin_ids = {id_: 1 if id_ in members_ids else 0 for id_ in all_ids}
            return pd.Series(bin_ids)
        else:
            return pd.Series(name2id)
