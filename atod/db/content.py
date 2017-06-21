import json

from atod.db import schemas, session
from atod import settings
# db models
from atod.db_models.hero import HeroModel
from atod.db_models.ability import AbilityModel
from atod.db_models.ability_specs import  AbilitySpecsModel
from atod.db_models.ability_texts import AbilityTextsModel
# utils
from atod.utils import txt2json, json2rows, abilities


def add_heroes(npc_heroes: str, patch: str):
    ''' Unite everything that is needed to add heroes to the db table.
     
    That method does: parses `raw_file` to json, extracts information from
    json according to heroes table schema, adds heroes to the table. 
    
    Args:
        npc_heroes: full path to the npc_heroes.txt file.
        patch: version of the game from which info was taken.
    '''
    heroes_file = npc_heroes

    heroes_dict = txt2json.to_json(heroes_file)

    rows = json2rows.heroes_to_rows(heroes_dict,
                                    schemas.get_heroes_columns())

    for row in rows:
        row['patch'] = patch
        hero = HeroModel(row)
        session.add(hero)

    session.commit()


def add_abilities_specs(npc_abilties: str, patch: str):
    ''' Fills table with the data from cleaned npc_abilities file. 
    
    Args:
        npc_abilties: full path to the npc_abilities.txt file.
        patch: version of the game from which info was taken.
        
    '''

    parsed = txt2json.to_json(npc_abilties)
    clean  = abilities.get_cleaned_abilities(parsed)

    schema = schemas.get_abilities_specs_columns()

    with open(settings.CONVERTER_FILE, 'r') as fp:
        converter = json.load(fp)

    for skill, description in clean.items():
        try:
            hero, skill_name = json2rows.parse_skill_name(skill)
        # if skill name cannot be parsed
        except ValueError:
            continue

        for row in json2rows.ability_to_row(description, schema):
            row['HeroID'] = converter[hero]
            row['name'] = skill_name
            row['pk'] = str(row['ID']) + '.' + str(row['lvl'])
            row['patch'] = patch

            skill = AbilitySpecsModel(row)
            session.add(skill)

    session.commit()


def add_abilities(labels: str, patch: str):
    ''' Fills abilities table. 
    
    Args:
        labels: full path to the labeled_abilities.json file
        patch: version of the data
    '''

    with open(labels, 'r') as fp:
        skills = json.load(fp)

    with open(settings.CONVERTER_FILE, 'r') as fp:
        converter = json.load(fp)

    for skill, description in skills.items():
        if 'special' in skill:
            continue

        # get skill and hero names
        try:
            hero, skill_name = json2rows.parse_skill_name(skill)
        except ValueError:
            continue

        # for marked abilities
        if 'labels' in description:
            row = json2rows.binarize_labels(description['labels'],
                                            schemas.LABELS)
        # for unmarked abilities
        else:
            row = {k: 0 for k in schemas.LABELS}

        row['HeroID'] = converter[hero]
        row['name'] = skill_name
        row['ID'] = description['ID']
        row['patch'] = patch

        skill = AbilityModel(row)
        session.add(skill)

    session.commit()


def add_abilities_texts(dota_english: str, patch):
    ''' Fills abilities_texts table.

    Notes:
        This function need AbilitiesTable to be created for current
        version. I will fix it in future versions.
        
    Args:
        dota_english: full path to the dota_english.txt file.
        patch: version of the game from which info was taken.
    '''

    for specification in get_abilities_texts(dota_english):
        # if specification is empty
        if not specification:
            continue

        specification['patch'] = patch
        texts = AbilityTextsModel(specification)
        session.add(texts)

        session.commit()


''' Functions below are doing utils of abilities texts and the reason
    they are here is because they need filled database tables (heroes and
    abilities).
'''
def group_abilities_texts(texts):
    ''' Groups the information in dota_english by ability.

        Args:
            texts (dict): *parsed* dota_english.txt

        Returns:
            desc_by_ability (dict): {<ability name>: <different descriptions>}
    '''

    desc_by_ability = dict()
    keys = sorted(texts)
    ability = ' '

    for key in keys:
        if ability in key:
            desc_by_ability[ability][key[len(ability) + 1:]] = texts[key]
        else:
            ability = key
            desc_by_ability[ability] = dict()
            desc_by_ability[ability]['name'] = texts[ability]

    return desc_by_ability


def get_abilities_texts(dota_english: str):
    ''' Produces ready to use dictionaries to create AbilityTextsModel object.

        Yields:
            dict: containing all the needed keys or empty if texts can not be
                  sorted
    '''

    texts_file    = dota_english
    # parse texts file and take only texts from it
    parsed_texts  = txt2json.to_json(texts_file)['lang']['Tokens']
    # group texts by ability
    grouped_texts = group_abilities_texts(parsed_texts)

    # for all keys in grouped_texts
    prefix = 'DOTA_Tooltip_ability_'
    for key in list(grouped_texts):
        if not key.startswith(prefix):
            del grouped_texts[key]
            continue

        # this is a tuple
        parsed_name = json2rows.parse_skill_name(key[len(prefix):])

        # there are 2 independent `if` statements to call parse_skill_name()
        # one time and only if it is needed

        # if the name cann't be parsed
        if len(parsed_name) < 2:
            del grouped_texts[key]
            continue
        # if the name can be split to the hero name and skill name -- change
        # original uppercase name to in-game style: all lower case with under
        # instead of space
        else:
            grouped_texts[key]['name'] = parsed_name[1]
            sorted_ = sort_texts(grouped_texts[key])
            id_ = get_id_from_in_game_name(parsed_name[0], parsed_name[1])
            if sorted_ and id_ is not None:
                sorted_['ID'] = id_
                yield sorted_
            else:
                yield {}


def sort_texts(unsorted):
    ''' Creates a dictionary that fits AbilityTextsModel init method.

        Args:
            unsorted (dict): all fields in dota_english file for an ability.

        Returns:
            dict: where keys are columns in AbilityTextsModel
    '''

    # description is the most important text, so if ability doesn't contain
    # one it wouldn't be added in db
    if 'Description' not in unsorted:
        return {}

    sorted_ = dict()
    sorted_['name'] = unsorted['name']
    sorted_['description'] = unsorted['Description']
    sorted_['lore'] = unsorted['Lore'] if 'Lore' in unsorted else ''

    sorted_['notes'] = ''
    sorted_['other'] = ''
    for key in unsorted:
        if 'Note' in key:
            # all notes are just sentences, so there is no need in special
            # delimiter
            sorted_['notes'] += unsorted[key] + ' '
        elif key.lower() not in sorted_:
            sorted_['other'] += unsorted[key] + ' | '

    return sorted_


def get_id_from_in_game_name(hero_name, skill_name):
    ''' Finds skill id.

        This function is needed to prevent collision: when a few heroes have
        skill with the same name.

        Args:
            hero_name (str): hero part of in-game ability name
            skill_name (str): skill part of in-game ability name

        Returns:
            int or None: int if id is found, None otherwise
    '''

    query = session.query(HeroModel.HeroID)
    hero_id = query.filter(HeroModel.in_game_name == hero_name).first()[0]

    query = session.query(AbilityModel.ID)
    ability_id_ = query.filter(AbilityModel.HeroID == hero_id,
                               AbilityModel.name == skill_name).first()

    if ability_id_ is None:
        return None
    else:
        return ability_id_[0]
