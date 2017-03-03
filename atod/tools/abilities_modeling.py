import json
import logging
from gensim import corpora, models

from atod import settings
from atod.tools.json2vectors import find_heroes_abilities, make_flat_dict
from atod.tools.abilities import get_encoding


logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


def extract_description(ability):
    ''' Converts ability to its string representation.

        :Args:
            ability (dict) : contains ability description

        :Returns:
            description (str) : created descrition
    '''
    description = []

    for key, value in ability.items():
        if isinstance(value, str):
            if 'special' not in value:
                description.extend([x.lower() for x in value.split(' ')])
        elif isinstance(value, float) or isinstance(value, list):
            description.extend([x.lower() for x in key.split('_')])

    return description


# IDEA: evarything should be class
def save_descriptions(dictionary, corpus):
    dictionary.save(settings.ABILITIES_DICT_FILE)
    corpora.MmCorpus.serialize(settings.ABILITIES_CORPUS_FILE, corpus)


def create_descriptions():
    ''' Creates corpora.Dictionary and corpora.Mmcorpus'''
    with open(settings.ABILITIES_FILE, 'r') as fp:
        data = json.load(fp)['DOTAAbilities']

    heroes_abilities_list = find_heroes_abilities(data)
    encoding = get_encoding()

    heroes_abilities = {}
    for ability in heroes_abilities_list:
        heroes_abilities[ability] = data[ability]

    descriptions = []
    for ability, parameters in heroes_abilities.items():
        flat = make_flat_dict(parameters)
        description = extract_description(flat)
        descriptions.append(description)

    dictionary = corpora.Dictionary(descriptions)
    corpus = [dictionary.doc2bow(d) for d in descriptions]

    return (dictionary, corpus)


def load_descriptions():
    dictionary = corpora.Dictionary.load(settings.ABILITIES_DICT_FILE)
    corpus = corpora.MmCorpus(settings.ABILITIES_CORPUS_FILE)

    return (dictionary, corpus)


def label():
    ''' Labels abilities and returns result. '''
    dictionary, corpus = load_descriptions()
    tfidf = models.TfidfModel(corpus)

    with open(settings.ABILITIES_FILE, 'r') as fp:
        data = json.load(fp)['DOTAAbilities']

    categories = ['armor', 'damage', 'illusion', 'transformation', 'move',
                  'stun', 'tick', 'pct', 'radius', 'speed', 'bonus']

    heroes_abilities_list = find_heroes_abilities(data)
    encoding = get_encoding()

    heroes_abilities = {}
    for ability in heroes_abilities_list:
        heroes_abilities[ability] = data[ability]

    descriptions = {}
    for ability in heroes_abilities:
        descriptions[ability] = []
        flat = make_flat_dict(heroes_abilities[ability])
        description = extract_description(flat)

        weights = tfidf[dictionary.doc2bow(description)]
        weights.sort(key=lambda tup: tup[1], reverse=True)

        weights_labels = [dictionary[w[0]] for w in weights]

        for w in weights:
            if w[0] in categories:
                descriptions[ability].append(dictionary[w[0]])
        if len(descriptions[ability]) < 3:
            for w in weights:
                if w[1] > 0.25 and w[0] not in descriptions[ability]:
                    descriptions[ability].append(dictionary[w[0]])
                else:
                    break

    return descriptions
