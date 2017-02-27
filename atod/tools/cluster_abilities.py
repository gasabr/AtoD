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

km = KMeans(n_clusters=20, random_state=42, max_iter=500).fit(data.values)

result = {}
for skill, cluster in zip(list(data.index), km.labels_):
    if not str(cluster) in result.keys():
        result[str(cluster)] = []
    result[str(cluster)].append(skill)

# write result to excel for further manual sort
filepath = os.path.join(settings.DATA_FOLDER + 'abilities_clusterisation.xlsx')
workbook = xlsxwriter.Workbook(filepath)
worksheet = workbook.add_worksheet()

for i, key in enumerate(result.keys()):
    worksheet.write(1, i, key)
    for j, value in enumerate(result[key]):
        worksheet.write(j+1, i, value)

workbook.close()
