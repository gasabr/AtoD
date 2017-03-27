''' This files reads labeled abilities from abilities_labeled.json,
    adds labels to abilities and writes this to other file.
'''
import json

from atod import settings


def add_labels():
    with open(settings.ABILITIES_LABELED_FILE, 'r') as fp:
        labeled = json.load(fp)['DOTAAbilities']

    with open(settings.CLEAN_ABILITIES_FILE, 'r') as fp:
        clean = json.load(fp)

    for ability, description in labeled.items():
        if 'labels' in description and \
                    ability in clean.keys():
            clean[ability]['labels'] = description['labels']

    with open(settings.TMP_ABILITIES, 'w+') as fp:
        json.dump(clean, fp, indent=2)


def status():
    ''' Prints how much abilities are labeled. '''
    with open(settings.TMP_ABILITIES, 'r') as fp:
        in_process = json.load(fp)

    labeled = 0

    for ability, description in in_process.items():
        if 'labels' in description:
            labeled += 1

    return '{}/{} abilities are labeled'.format(labeled, len(in_process))

if __name__ == '__main__':
    print(status())