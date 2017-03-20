#!/usr/bin/env python
import json
import numpy as np
from sklearn.cluster import DBSCAN, KMeans
from sklearn.preprocessing import StandardScaler
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

    # mm_scaler = StandardScaler()
    # data_norm = mm_scaler.fit_transform(data.values)

    # can be used to find trash or VERY-VERY similar abilities
    # clustering = DBSCAN(eps=10, min_samples=3).fit(data.values)
    clustering = KMeans(n_clusters=45, max_iter=500).fit(data.values)

    result = {}
    for skill, cluster in zip(list(data.index), clustering.labels_):
        if not str(cluster) in result.keys():
            result[str(cluster)] = []
        result[str(cluster)].append(skill)

    print(json.dumps(result, indent=2))
    # print(data.loc['earthshaker_fissure'].to_string())


def cluster():
    # load labeled abilities
    train_x, train_y, test_x = Abilities.load_train_test()

    ovr = OneVsRestClassifier(SVC(kernel='poly'))

    Y = np.asarray(train_y, dtype='float64')
    X_train = train_x.values
    ovr.fit(X_train, Y)
    prediction = ovr.predict(test_x.values)
    for row, pre in zip(test_x.iterrows(), prediction):
        print(row[0], [l for p, l in zip(pre, settings.LABELS) if p == 1])


if __name__ == '__main__':
    cluster_binary()
