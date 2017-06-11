#!/usr/bin/env python3
''' Extracts picks from the huge matches dump. '''

import json


def main():
    matches = dict()
    with open('matches.jsonlines', 'r') as f:
        for line in f:
            match_info = json.loads(line)

            try:
                picks = filter(lambda x: x['is_pick'], match_info['picks_bans'])
            except TypeError:
                continue

            match_id = match_info['match_id']
            matches[match_id] = dict()
            matches[match_id]['radiant_win'] = match_info['finish']['radiant_win']
            matches['1'] = matches['0'] = list()

            for pick in picks:
                matches[match_id].setdefault(pick['team'], [])
                matches[match_id][pick['team']].append(pick['hero_id'])

    with open('picks.json', 'w+') as fp:
        json.dump(matches, fp, indent=2)


if __name__ == '__main__':
    main()
