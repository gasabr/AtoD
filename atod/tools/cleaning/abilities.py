''' This script cleans npc_abilities.json file by:
    - removing skill name from description
    - replacing lists with their avg value
    - merging rare properties to popular
'''

import json
import re

from atod import settings


def clean_properties():
    remove_skills_names()
    merge_similar()
    min_max2avg()
    merge_rare()


def find_skills(raw_abilities):
    ''' Finds skills in dictionary.

        'Skills' does **not** include scepter upgrades, empty or hidden
        abilities.

        Args:
            raw_abilities (dict): content of npc_abilities.json

        Returns:
            skills (dict): heroes abilities in `raw_abilities`
    '''
    # load converter to get heroes names
    with open(settings.IN_GAME_CONVERTER, 'r') as fp:
        converter = json.load(fp)

    heroes_names = [c for c in converter.keys()
                    if re.findall(r'[a-zA-Z|\_]+', c)]

    # find all the heroes skills, but not talents
    skills_list = []
    for key, value in raw_abilities['DOTAAbilities'].items():
        # if ability contains hero name, doesn't contain special_bonus
        if any(map(lambda name: name in key, heroes_names)) and \
                        'special_bonus' not in key and \
                        'hidden' not in key and \
                        'empty' not in key and \
                        'scepter' not in key and \
                        key != 'Version':
            skills_list.append(key)

    skills = {}
    for ability in skills_list:
        skills[ability] = raw['DOTAAbilities'][ability]

    return skills


def remove_skills_names():
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


def merge_similar():
    pass


def min_max2avg():
    pass


def merge_rare():
    pass


def show_current_progress(stage_name):
    ''' Function logs (prints) info about current stage of cleaning.

        This is needed to understand what is going on with data after
        each stage of cleaning: how an amount of keys has changed...

        Args:
            stage_name (str): to understand what log is about
    '''

    print()

if __name__ == '__main__':
    with open(settings.ABILITIES_FILE, 'r') as fp:
        raw = json.load(fp)

    skills = find_skills(raw)
