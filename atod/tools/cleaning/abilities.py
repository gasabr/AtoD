''' This script cleans npc_abilities.json file by:
    - removing skill name from description
    - replacing lists with their avg value
    - merging rare properties to popular
'''

import re
import json
import logging

from atod import settings
from atod.tools.dictionary import all_keys, make_flat_dict


logging.basicConfig(level=logging.DEBUG)


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
    stop_words = ['special_bonus', 'hidden', 'empty', 'scepter', 'voodoo',
                  'stop', 'self', 'cancel', 'throw', 'return', 'release',
                  'brake', 'end']

    # find all the heroes skills, but not talents
    skills_list = []
    for key, value in raw_abilities['DOTAAbilities'].items():
        # if ability contains hero name, doesn't contain stop words
        if any(map(lambda name: name in key, heroes_names)) and \
                not any(map(lambda word: word in key, stop_words)) and \
                key != 'Version':
            skills_list.append(key)

    skills = {}
    for ability in skills_list:
        skills[ability] = raw_abilities['DOTAAbilities'][ability]

    return skills


def remove_skills_names(skills):
    ''' Removes parts of ability name from all the properties.

        There are a lot of skills which properties looks like this:
        <skillname>_<property>, they could be simplified to <property>.
        This function does exactly that.

        Args:
            skills (dict): flat dictionary of heroes abilities

        Returns:
            clean (dict): cleaned skills dictionary, where every changed
                ability has special keyword `changed`.
    '''

    for skill, description in skills.items():
        skill_changed = False
        for property_ in list(description):
            property_split = property_.split('_')
            new_name_list = [p for p in property_split if p not in skill]

            if new_name_list != property_split and len(new_name_list) != 0:
                new_name = ''.join([n + '_' for n in new_name_list]).strip('_')
                skills[skill][new_name] = description[property_]
                del skills[skill][property_]
                skill_changed = True

            else:
                continue

        if skill_changed:
            skills[skill]['changed'] = True

    return skills


def change_properties(skills):
    ''' Applies abilities_changes.json to skills.

        abilities_changes.json - dict where key is name if old
        property and corresponding value is the new property.
        If value == '' property will be removed.

        Args:
            skills (dict): flat dictionary of skills

        Returns:
            skills_ (dict): with changed properties
    '''

    skills_ = skills.copy()
    with open(settings.ABILITIES_CHANGES_FILE, 'r') as fp:
        changes = json.load(fp)

    for skill in skills:
        for prop in list(skills_[skill]):
            if prop not in changes.keys():
                continue
            elif changes[prop] == '':
                del skills_[skill][prop]
                continue
            else:
                skills_[skill][changes[prop]] = skills_[skill][prop]
                del skills_[skill][prop]

    return skills_


def average_properties(skills):
    ''' Averages properties values where it's possible.

        Args:
            skills (dict): flat dict of skills

        Returns:
            skills_ (dict): the same dict, where abilities changed
                according to rule in `min_max2avg` docstring.
    '''

    for ability, description in skills.items():
        if any(map(lambda x: 'max' in x, description)):
            skills[ability] = min_max2avg(description)

    return skills


def min_max2avg(description):
    ''' Converts min and max properties to one containing their avg.

        Args:
            description (dict): ability properties

        Returns:
            desc (dict): changed dict

        Examples:
            >>> d = {'min_stun': 1, 'max_stun': 2}
            >>> d_ = min_max2avg(d)
            {'stun': 1.5, 'changed': True}
    '''

    desc = description.copy()
    for property_, value in description.items():
        if 'max' in property_:
            partition = property_.partition('max')
            min_prop = partition[0] + 'min' + partition[2]
            if min_prop in desc.keys():
                new_prop = (partition[0].rstrip('_') + partition[2]).strip('_')
                desc[new_prop] = (value + description[min_prop]) / 2
                desc['changed'] = True
                del desc[min_prop]
                del desc[property_]

    return desc


def clean_properties(dict_, word, remove_prop=False):
    ''' Remove word from property or the whole property. '''
    for key, value in dict_.items():
        for k in list(value):
            if word in k:
                if not remove_prop:
                    new_k = remove_word(k, word)
                    value[new_k] = value[k]
                del value[k]

    return dict_


def remove_word(phrase, word):
    partition = phrase.partition(word)
    new_phrase = partition[0].strip('_') + '_' \
            + partition[2].strip('_')
    new_phrase = new_phrase.strip('_')

    return new_phrase


def clean_move_properties(dict_):
    remove_words = ('movement', 'movespeed', 'speed', 'move')
    for ability, description in dict_.items():
        for key in list(description):
            new_key = key
            if 'move' in key:
                for word in remove_words:
                    partition = new_key.partition(word)
                    new_key = partition[0].strip('_') \
                            + partition[2].rstrip('_')
                new_key = ('movespeed_' + new_key.lstrip('_')).rstrip('_')

                dict_[ability][new_key] = dict_[ability][key]
                del dict_[ability][key]

    return dict_


def show_progress(stage_name, abilities):
    ''' Function logs (prints) info about current stage of cleaning.

        This is needed to understand what is going on with data after
        each stage of cleaning: how an amount of keys has changed...

        Args:
            stage_name (str): will be printed before log message
            abilities (dict): current stage of abilities cleaning
    '''

    logging.info('================================================')
    logging.info('stage - {}'.format(stage_name))
    logging.info('#abilities = {}'.format(len(abilities)))
    n_keys = len(set(all_keys(abilities, include_dict_keys=False)))
    logging.info('#keys = {}'.format(n_keys))
    logging.info('================================================\n')


def clean():
    with open(settings.ABILITIES_FILE, 'r') as fp:
        raw = json.load(fp)
    show_progress('RAW', raw)

    # find heroes abilities
    skills_nested = find_skills(raw)
    show_progress('SKILLS', skills_nested)

    # make skills flat
    skills = {}
    for ability, description in skills_nested.items():
        skills[ability] = make_flat_dict(description)
    show_progress('FLAT', skills)

    # remove ability name from its properties
    skills = remove_skills_names(skills)
    show_progress('CLEANING 1', skills)

    # convert min and max properties to their avg
    skills = average_properties(skills)
    show_progress('MIN MAX -> AVG', skills)

    # remove tooltip properties from skills
    skills = clean_properties(skills, word='tooltip')
    skills = clean_properties(skills, word='scepter', remove_prop=True)
    show_progress('CLEANING PROPERTIES', skills)

    # clean movespeed properties
    skills = clean_move_properties(skills)
    show_progress('CLEANING MOVE PROPERTIES', skills)

    # map properties
    skills = change_properties(skills)
    show_progress('CLEANING 2', skills)

    return skills


if __name__ == '__main__':
    clean_abilities = clean()
    # with open(settings.CLEAN_ABILITIES_FILE, 'w+') as fp:
    #     json.dump(clean_abilities, fp, indent=2)
