''' Module for updating information in the db.'''
import os
import json

from atod import settings
from atod.preprocessing.txt2json import to_json
from atod.preprocessing.clean_abilities import clean


needed_files = ['npc_heroes.txt', 'npc_abilities.txt',
                'abilities_labeling.json']

# TODO: add versbose option which will set logging level to INFO
def update_abilities(file, version):
    ''' Updates `version`_abilities and `version`_abilities_specs tables. 
    
        Raises:
            FileNotFoundError if file doesn't exists
    
        Args:
            file (str): absolute path to file npc_abilities.txt
            version (str): game version, will be used as prefix for the 
                database tables
    '''

    if not os.path.exists(file):
        raise FileNotFoundError(file + 'not found.')

    as_json = to_json(file)
    clean_  = clean(data=as_json)



def update(folder=''):
    ''' Updates data in the database from files in `folder`.
    
        Files needed for update: 
            * items.txt
            * npc_heroes.txt
            * npc_abilities.txt
            * abilities_labeling.json -- dictionary skill -> labels
            
        Raises:
            FileExistsError if folder doesn't exists
    
        Args:
            folder (str): WILL BE USED AS VERSION NAME. absolute path to 
                folder containing files for the update.
    '''

    # check folder existence
    # check that all needed files are in the folder
    for path in needed_files:
        full_path = os.path.join(folder, path)
        if not os.path.exists(full_path):
            raise FileExistsError(full_path + 'file not found.')

    # update_abilities()

    # update_heroes()
    pass


if __name__ == '__main__':
    update_abilities('/Users/gasabr/AtoD/atod/data/raw/npc_abilities.json',
                     '702b')