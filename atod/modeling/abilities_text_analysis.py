import json
import logging

from gensim import corpora, models
from sklearn.feature_extraction.text import TfidfVectorizer

from atod import settings
from atod.preprocessing.abilities_old import abilities as Abilities
from atod.preprocessing.dictionary import make_flat_dict

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',
                    level=logging.INFO)
logger = logging.getLogger()

abilities_specials = Abilities.specials
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


def get_words_weights():
    # training vectorizer part
    # get all the words in properties
    properties_as_words = set()
    properties_sorted = set()
    for ability_name, specials in abilities_specials.items():
        for special in specials:
            # property with '_' replaced with ' '
            as_words = special.replace('_', ' ')
            # add all the words from property key to words
            properties_as_words.update([as_words])

            sorted_words = tuple(sorted([w for w in as_words.split()]))
            # add to sorted properties ability name and tuple of sorted words
            properties_sorted.update([(ability_name, special, sorted_words)])

    # initialize and fit vectorizer
    v = TfidfVectorizer().fit(properties_as_words)

    words_weights = dict()
    for ability_name, special, pr in properties_sorted:
        # getting weights part
        as_string  = ''.join([p + ' ' for p in pr])
        # property_ = list(abilities[as_string].keys())[0].replace('_', ' ')
        weights = v.transform([as_string])

        if ability_name not in words_weights.keys():
            words_weights[ability_name] = dict()

        for word in as_string.split():
            if any(map(lambda number: word == str(number), range(10))):
                continue
            word2weight = (word, weights[0, v.vocabulary_.get(str(word))])
            if not special in words_weights[ability_name].keys():
                words_weights[ability_name][special] = []
            words_weights[ability_name][special].append(word2weight)

    return words_weights


# IDEA: everything should be class
def save_descriptions(dictionary, corpus):
    '''Saves corpora.Dictionary and corpora.Mmcorpus.'''
    dictionary.save(settings.ABILITIES_DICT_FILE)
    corpora.MmCorpus.serialize(settings.ABILITIES_CORPUS_FILE, corpus)


def create_descriptions():
    '''Creates corpora.Dictionary and corpora.Mmcorpus.'''
    heroes_abilities = Abilities.clean_properties()

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

label(write_to_file=True)