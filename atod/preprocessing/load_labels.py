import json
from sklearn.preprocessing import MultiLabelBinarizer

from atod.settings import TMP_ABILITIES
''' Module load training data from labeled_abilities.json.'''

def load_binary_labels():
    ''' Isn't used right now.
        Creates mapping ability_name -> binarized labels.

        Returns:
            ability2labels (dict): described above mapping.
    '''
    with open(TMP_ABILITIES, 'r') as fp:
        abilities = json.load(fp)

    labels = [d['labels'] for _, d in abilities.items() if 'labels' in d]
    binarizer = MultiLabelBinarizer().fit(labels)

    ability2labels = {}
    for a in abilities:
        if 'labels' in abilities[a]:
            transformed = binarizer.transform([abilities[a]['labels']])
            ability2labels[a] = transformed[0].tolist()

    return ability2labels


def load_labels():
    ''' Loads labeling from abilities_labeled.json. '''
    with open(TMP_ABILITIES, 'r') as fp:
        abilities = json.load(fp)

    return {k: v['labels'] for k, v in abilities.items()
                           if 'labels' in v
                           and v['labels'] != [-1]}


load_binary_labels()