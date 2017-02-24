#!/usr/bin/env python
import json
from sklearn.cluster import KMeans

from atod.settings import ABILITIES_FILE
from json2vectors import to_bin_vectors

categorical_features = [
    "AbilityUnitDamageType",
    "AbilityModifierSupportValue",
    "AbilityBehavior",
    "SpellImmunityType",
    "SpellDispellableType": "SPELL_DISPELLABLE_NO",
    "FightRecapLevel",
]

data = to_bin_vectors(ABILITIES_FILE)

print(data.info)

data.drop(categorical_features)

km = KMeans(n_clusters=8, random_state=42).fit(data.values)

result = {}
for skill, cluster in zip(list(data.index), km.labels_):
    if not str(cluster) in result.keys():
        result[str(cluster)] = []
    result[str(cluster)].append(skill)

# print(km.labels_)

print(json.dumps(result, indent=2))
