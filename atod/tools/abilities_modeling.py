import json
import logging
from gensim import corpora, models

from atod import settings
from atod.tools.dictionary import make_flat_dict
from atod.abilities import abilities as Abilities


logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',
                    level=logging.INFO)
logger = logging.getLogger()

abilities_by_manacost = Abilities.clustering_by('AbilityManaCost')
abilities_by_cooldown = Abilities.clustering_by('AbilityCooldown')

special_words = ['bonus', 'reduction', 'per', 'sec', 'regen', 'chance',
                 'tooltip']

def extract_description(ability, properties):
    ''' Converts ability dictionary to list of words in it.

        Args:
            ability (str) : ability name to search in clustering
            properties (dict): flat dict of properties

        Returns:
            description (str) : created description
    '''
    description = []

    for key, value in properties.items():
        if key == 'AbilityCooldown':
            description.append(abilities_by_cooldown[ability])
            continue

        if key == 'AbilityManaCost':
            description.append(abilities_by_manacost[ability])
            continue

        # if any of special words in key - add it to the description as it is
        if any(map(lambda w: w in key, special_words)):
            description.append(key)
            continue

        # add string description of some property as it is
        if isinstance(value, str):
            if 'special' not in value:
                description.extend([x.lower() for x in value.split(' ')])

        # if the value isn't string - add words in key to the description
        elif isinstance(value, float) or isinstance(value, list):
            description.extend([x.lower() for x in key.split('_')])

    return description


# IDEA: everything should be class
def save_descriptions(dictionary, corpus):
    '''Saves corpora.Dictionary and corpora.Mmcorpus.'''
    dictionary.save(settings.ABILITIES_DICT_FILE)
    corpora.MmCorpus.serialize(settings.ABILITIES_CORPUS_FILE, corpus)


def create_descriptions():
    '''Creates corpora.Dictionary and corpora.Mmcorpus.'''
    heroes_abilities = Abilities.skills

    descriptions = []
    for ability, parameters in heroes_abilities.items():
        flat = make_flat_dict(parameters)
        description = extract_description(ability, flat)
        descriptions.append(description)

    dictionary = corpora.Dictionary(descriptions)
    corpus = [dictionary.doc2bow(d) for d in descriptions]

    return dictionary, corpus


def load_descriptions():
    '''Loads corpora.Dictionary and corpora.Mmcorpus.'''
    dictionary = corpora.Dictionary.load(settings.ABILITIES_DICT_FILE)
    corpus = corpora.MmCorpus(settings.ABILITIES_CORPUS_FILE)

    return dictionary, corpus


def label(write_to_file=False):
    '''Labels abilities and returns result.'''
    dictionary, corpus = create_descriptions()
    tfidf = models.TfidfModel(corpus)

    categories = ['armor', 'damage', 'illusion', 'transformation', 'move',
                  'stun', 'tick', 'pct', 'radius', 'speed', 'bonus',
                  'reduction', 'silence']

    heroes_abilities = Abilities.skills

    descriptions = {}
    for ability in heroes_abilities:
        descriptions[ability] = []
        description = extract_description(ability, heroes_abilities[ability])

        weights = tfidf[dictionary.doc2bow(description)]
        weights.sort(key=lambda tup: tup[1], reverse=True)

        for w in weights:
            if dictionary[w[0]] in categories:
                descriptions[ability].append(dictionary[w[0]])
        if len(descriptions[ability]) < 3:
            for w in weights:
                if w[1] > 0.25 and w[0] not in descriptions[ability]:
                    descriptions[ability].append(dictionary[w[0]])
                else:
                    break

    if write_to_file:
        with open(settings.ABILITIES_LABELING_FILE, 'w+') as fp:
            json.dump(descriptions, fp, indent=2)

    return descriptions

label()