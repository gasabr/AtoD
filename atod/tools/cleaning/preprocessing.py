import json
from sklearn.preprocessing import MultiLabelBinarizer

from atod.settings import ABILITIES_TRAIN_FILE
''' Module load training data from labeled_abilities.json.'''

def load_binary_labels():
    ''' Isn't used right now.
        Creates mapping ability_name -> binarized labels.

        Returns:
            ability2labels (dict): described above mapping.
    '''
    with open(ABILITIES_TRAIN_FILE, 'r') as fp:
        abilities = json.load(fp)['DOTAAbilities']

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
    with open(ABILITIES_TRAIN_FILE, 'r') as fp:
        abilities = json.load(fp)['DOTAAbilities']

    return {k: v['labels'] for k, v in abilities.items()
                           if 'labels' in v}