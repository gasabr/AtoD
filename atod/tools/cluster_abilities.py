#!/usr/bin/env python
import os
import json
import xlsxwriter
from sklearn.cluster import KMeans, DBSCAN

from atod import settings
from json2vectors import to_bin_vectors, to_vectors

categorical_features = [
    "AbilityUnitDamageType",
    "AbilityModifierSupportValue",
    "AbilityBehavior",
    "SpellImmunityType",
    "SpellDispellableType",
    "FightRecapLevel",
]


# TODO: write my own metric for db scan

def cluster_binary():
    data = to_bin_vectors(settings.ABILITIES_FILE)

    km = KMeans(n_clusters=35, random_state=100, max_iter=500).fit(data.values)
    dbscan = DBSCAN(eps=1, min_samples=2).fit(data.values)

    result = {}
    for skill, cluster in zip(list(data.index), dbscan.labels_):
        if not str(cluster) in result.keys():
            result[str(cluster)] = []
        result[str(cluster)].append(skill)

    print(json.dumps(result, indent=2))


def to_excel(clusters, filename):
    ''' Writes clusterization to excel file, column = cluster'''
    # write result to excel for further manual sort
    filepath = os.path.join()
    workbook = xlsxwriter.Workbook(filepath)
    worksheet = workbook.add_worksheet()

    for i, key in enumerate(result.keys()):
        worksheet.write(1, i, key)
        for j, value in enumerate(result[key]):
            worksheet.write(j+1, i, value)

    workbook.close()


if __name__ == '__main__':
    cluster_binary()
