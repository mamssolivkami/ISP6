import numpy as np
from hierarchy import *


ALTERNATIVES = ['a1', 'a2', 'a3', 'a4']

CRITERIA_IMPORTANCE = {
    'k1': 7,
    'k2': 5,
    'k3': 1,
    'k4': 3
}

ALTERNATIVES_BY_CRITERIA = {
    'k1': {
        'a1': 3,
        'a2': 5,
        'a3': 9,
        'a4': 11
    },
    'k2': {
        'a1': 11,
        'a2': 9,
        'a3': 7,
        'a4': 5
    },
    'k3': {
        'a1': 9,
        'a2': 7,
        'a3': 5,
        'a4': 3
    },
    'k4': {
        'a1': 7,
        'a2': 11,
        'a3': 3,
        'a4': 1
    }
}


def _compare_criteria(a, b):
    if a > b:
        return a - b
    if a == b:
        return 1

    return 1 / (b - a)


def importance_to_matrix(item_to_importance: dict, name=None):
    items = list(item_to_importance.keys())
    items_count = len(items)

    matrix = np.zeros([items_count, items_count])

    for i in range(items_count):
        for j in range(items_count):
            if i == j:
                matrix[i, j] = 1
                continue

            c_row = items[i]
            c_col = items[j]

            matrix[i, j] = _compare_criteria(
                item_to_importance[c_row],
                item_to_importance[c_col]
            )

    return MatrixTable(items, items, matrix, name)


def get_criteria_table():
    return importance_to_matrix(CRITERIA_IMPORTANCE)


def get_alternatives_comparisons():
    comparisons = {}

    for criteria, alts in ALTERNATIVES_BY_CRITERIA.items():
        table = importance_to_matrix(alts, criteria)
        comparisons[criteria] = table

    return comparisons
