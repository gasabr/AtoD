#!/usr/bin/env python
import json
from sklearn.cluster import DBSCAN, KMeans

from atod.abilities import abilities as Abilities

categorical_features = [
    "AbilityUnitDamageType",
    "AbilityModifierSupportValue",
    "AbilityBehavior",
    "SpellImmunityType",
    "SpellDispellableType",
    "FightRecapLevel",
]


def cluster_binary():
    data = Abilities.frame

    # print(list(data.columns))

    dbscan = DBSCAN(eps=1, min_samples=2).fit(data.values)
    # km = KMeans(n_clusters=35, max_iter=500).fit(data.values)

    result = {}
    for skill, cluster in zip(list(data.index), dbscan.labels_):
        if not str(cluster) in result.keys():
            result[str(cluster)] = []
        result[str(cluster)].append(skill)

    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    cluster_binary()
