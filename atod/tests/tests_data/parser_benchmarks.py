''' This file checks how fast my parser works.'''

import time

from numpy.linalg import solve

from atod.utils import files
from atod.utils.txt2json import to_json


def time_parser(filename):
    start = time.time()
    to_json(filename)
    end   = time.time()

    return end - start


def file_len(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        for i, l in enumerate(f):
            pass
    return i + 1


if __name__ == '__main__':
    files_ = [files.get_abilities_texts_file(),
              files.get_abilities_file(),
              files.get_heroes_file(),
              files.get_shops_file()]

    for file in files_:
        n_lines = file_len(file)
        time_   = time_parser(file)
        print(n_lines, time_)

    counters = [[34, 361, 2, 21963],
                [0, 11075, 5626, 14277],
                [0, 94, 1844, 15387],
                [0, 4, 15, 214]]

    times = [265, 235, 126, 2]

    solution = solve(counters, times)
    print(solution)
