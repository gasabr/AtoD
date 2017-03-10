from sklearn.feature_extraction.text import TfidfVectorizer

from atod.abilities import abilities as Abilities


abilities_specials = Abilities.specials

# set of properties as strings
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