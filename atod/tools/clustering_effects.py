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


# oneside_effects = ['stun', 'silence', 'bash']
# weights = get_words_weights()
# for ability, description in weights.items():
#     if 'slardar' not in ability:
#         continue
#     print(ability)
#     for d in description:
#         # if d in oneside_effects:
#         #     print(d)
#         #     continue
#         description[d].sort(key=lambda x: x[1])
#         print(description[d])

# FIXME: length of strings in function
def clean_damage_properties():
    ''' Cleans descriptions of abilities connected with damage.

        There are a lot of skills which properties looks like this:
        <skillname>_damage, but in the majority of cases it's just
        ability damage. This function converts such properties to
        Ability damage, if possible.

        Returns:
            changed (dict): changed skills dictionary, where every changed
                ability has special keyword `changed`.
    '''
    changed = Abilities.skills
    for skill, description in changed.items():
        skill_changed = False
        for property_ in description:
            # select possible keys
            if 'damage' in property_ or 'Damage' in property_ \
                    and 'DamageType' not in property_:
                property_split = property_.split('_damage')

                # if property contain any part of ability name
                if property_split[0] in skill:
                    # mark ability as changed
                    skill_changed = True
                    # cut ability name form property
                    new_property_name = property_[len(property_split[0]) + 1:]
                    # if new name contain only 'damage' and `AbilityDamage` is
                    # empty for this ability
                    if new_property_name == 'damage' and \
                                not 'AbilityDamage' in description.keys():
                        # set `AbilityDamage` to the old property value
                        changed[skill]['AbilityDamage'] = description[property_]
                        # delete the old property
                        del changed[skill][property_]
                        continue

                    # if `AbilityDamage` already exists or there are some
                    # additional words in property - create new property
                    changed[skill][new_property_name] = description[property_]
                    # and delete the old property
                    del changed[skill][property_]
                    continue
        if skill_changed:
            changed[skill]['changed'] = True

    return changed