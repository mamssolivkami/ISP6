from .core import *
from . import validation

import math_helpers


_RANDOM_ACCORDANCE_COEFFICIENTS = [
    0,
    0,
    0.58,
    0.9,
    1.12,
    1.24,
    1.32,
    1.41,
    1.45,
    1.49
]

def _get_random_accordance(matrix_size):
    return _RANDOM_ACCORDANCE_COEFFICIENTS[matrix_size - 1]


class TableAnalysis:
    def __init__(self, table: MatrixTable, col_sums: dict, row_geom_avgs: dict, norm_vector: dict, k, accordance_index, accordance_ratio):
        self.table = table

        self.sums_by_column = col_sums
        self.geometric_averages_by_row = row_geom_avgs

        self.norm_vector = norm_vector

        self.k = k
        self.accordance_index = accordance_index
        self.accordance_ratio = accordance_ratio


class Analysis:
    def __init__(
            self, table: MatrixTable,
            criteria_norm_vector, priorities,
            accordance_indices, general_accordance_index, general_accordance_ratio
    ):
        self.table = table

        self.criteria_norm_vector = criteria_norm_vector
        self.priorities = priorities

        self.accordance_indices = accordance_indices
        self.general_accordance_index = general_accordance_index
        self.general_accordance_ratio = general_accordance_ratio


def _sum_by_columns(table: MatrixTable):
    sums = {}

    for col in table.columns:
        sum = 0

        for row in table.rows:
            sum += table[row, col]

        sums[col] = sum

    return sums


def _geom_avg_by_rows(table: MatrixTable):
    avgs = {}

    for row in table.rows:
        avgs[row] = math_helpers.geom_avg(table.row_to_dict(row).values())

    return avgs


def _find_norm_vector(geom_avgs, geom_avg_sum):
    return dict((item, g_avg / geom_avg_sum) for item, g_avg in geom_avgs.items())


def analyze_table(table: MatrixTable, criteria_count=None):
    if criteria_count is None:
        criteria_count = len(table.rows)

    row_avgs = _geom_avg_by_rows(table)
    col_sums = _sum_by_columns(table)

    row_avgs_sum = row_avgs.values()
    geom_avg_sum = sum(row_avgs_sum)

    norm_vector = _find_norm_vector(row_avgs, geom_avg_sum)

    k = math_helpers.sum_product(col_sums, norm_vector)
    accordance_index = (k - criteria_count) / (criteria_count - 1)
    accordance_ratio = accordance_index / _get_random_accordance(len(table.rows))

    return TableAnalysis(table, col_sums, row_avgs, norm_vector, k, accordance_index, accordance_ratio)


def _get_alt_norm_vector(alt, alternative_table_analysis_dict: dict):
    criteria_to_norm_value = {}

    for criteria, analysis in alternative_table_analysis_dict:
        criteria_to_norm_value[criteria] = analysis.norm_vector[alt]


def _calc_priorities(alternatives, norm_vector, criteria_to_norms):
    return dict((alt, math_helpers.sum_product(norm_vector, criteria_to_norms.row_to_dict(alt))) for alt in alternatives)


def _get_criteria_accordance_indices(alternative_table_analysis_dict: dict):
    return dict((criteria, analysis.accordance_index) for criteria, analysis in alternative_table_analysis_dict.items())


def _calc_general_accordance_index(norm_vector: dict, criteria_accordance_indices: dict):
    return math_helpers.sum_product(norm_vector, criteria_accordance_indices)


def _calc_general_accordance_ratio(general_accordance_index, matrix_size):
    return general_accordance_index / _get_random_accordance(matrix_size)


def analyze_all(
        alternatives: list,
        criteria_table_analysis: TableAnalysis,
        alternative_table_analysis_dict: dict
    ):
    alt_criteria_norms = MatrixTable(alternatives, list(alternative_table_analysis_dict.keys()))

    for criteria, criteria_analysis in alternative_table_analysis_dict.items():
        for alt in alternatives:
            alt_criteria_norms[alt, criteria] = criteria_analysis.norm_vector[alt]

    norm_vector = criteria_table_analysis.norm_vector

    alt_priorities = _calc_priorities(alternatives, norm_vector, alt_criteria_norms)
    accordance_indices = _get_criteria_accordance_indices(alternative_table_analysis_dict)

    general_accordance_index = _calc_general_accordance_index(norm_vector, accordance_indices)
    general_accordance_ratio = _calc_general_accordance_ratio(general_accordance_index, len(alternatives))

    return Analysis(
        alt_criteria_norms,
        norm_vector, alt_priorities,
        accordance_indices,
        general_accordance_index, general_accordance_ratio
    )

