#!/usr/bin/env python
import json
import numpy as np
from sklearn.cluster import DBSCAN, KMeans
from sklearn.preprocessing import MinMaxScaler
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import SVC

from atod import settings
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
    # load labeled abilities
    data = Abilities.clean_frame

    mm_scaler = MinMaxScaler()
    data_norm = mm_scaler.fit_transform(data.values)

    # can be used to find trash or VERY-VERY similar abilities
    # clustering = DBSCAN(eps=10, min_samples=3).fit(data.values)
    clustering = KMeans(n_clusters=45, max_iter=500).fit(data_norm)

    result = {}
    for skill, cluster in zip(list(data.index), clustering.labels_):
        if not str(cluster) in result.keys():
            result[str(cluster)] = []
        result[str(cluster)].append(skill)

    print(json.dumps(result, indent=2))
    print(data.loc['earthshaker_fissure'].to_string())


def cluster():
    # load labeled abilities
    train_x, train_y, test_x = Abilities.load_train_test()

    ovr = OneVsRestClassifier(SVC(random_state=0))

    ovr.fit(train_x, train_y)
    prediction = ovr.predict(test_x.values)
    # print(prediction)
    for row, pre in zip(test_x.iterrows(), prediction):
        print(row[0], pre)


if __name__ == '__main__':
    cluster()
