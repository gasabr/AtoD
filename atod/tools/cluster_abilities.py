#!/usr/bin/env python
import os
import json
import xlsxwriter
from sklearn.cluster import KMeans

from atod import settings
from json2vectors import to_bin_vectors

categorical_features = [
    "AbilityUnitDamageType",
    "AbilityModifierSupportValue",
    "AbilityBehavior",
    "SpellImmunityType",
    "SpellDispellableType",
    "FightRecapLevel",
]

data = to_bin_vectors(settings.ABILITIES_FILE)

km = KMeans(n_clusters=28, random_state=42, max_iter=500).fit(data.values)

result = {}
for skill, cluster in zip(list(data.index), km.labels_):
    if not str(cluster) in result.keys():
        result[str(cluster)] = []
    result[str(cluster)].append(skill)

print(json.dumps(result, indent=2))
write_to = settings.DATA_FOLDER + 'abilities_clusterisation.xlsx'

def to_excel(clusters, filename):
    ''' Writes clusterization to excel file column = cluster'''
    write result to excel for further manual sort
    filepath = os.path.join()
    workbook = xlsxwriter.Workbook(filepath)
    worksheet = workbook.add_worksheet()

    for i, key in enumerate(result.keys()):
        worksheet.write(1, i, key)
        for j, value in enumerate(result[key]):
            worksheet.write(j+1, i, value)

    workbook.close()
