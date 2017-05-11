#!/usr/bin/env python
import json

from sklearn.cluster import KMeans
from sklearn.multiclass import OneVsRestClassifier
from sklearn.preprocessing import MinMaxScaler
from sklearn.svm import SVC

categorical_features = [
    "AbilityUnitDamageType",
    "AbilityModifierSupportValue",
    "AbilityBehavior",
    "SpellImmunityType",
    "SpellDispellableType",
    "FightRecapLevel",
]


if __name__ == '__main__':
    pass
