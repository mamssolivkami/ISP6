from .core import *


def _collections_equal(first, second):
    if len(first) != len(second):
        return False

    for i in range(len(first)):
        if first[i] != second[i]:
            return False

    return True


def _validate_tables(table: MatrixTable, str_source):
    for row in table.rows:
        for col in table.columns:
            if row == col and table[row, col] != 1:
                raise ValueError(f'Elements of equal rows and columns must equal 1. Source: {str_source}')

            if table[row, col] < 0 or table[col, row] < 0:
                raise ValueError(f'All elements of tables must be greater than 0. Source: {str_source}')

            if 1 / table[row, col] != table[col, row] or 1 / table[col, row] != table[row, col]:
                raise ValueError(f'All diagonal must follow the next rule:'
                                 f'table[row, col] == 1 / table[col, row].'
                                 f'Source: {str_source}'
                                 )


def validate_analysis(criteria_table: MatrixTable, criteria_comparisons):
    criteria_comparison_rows_columns = 'Rows and columns between all criteria comparisons must be same elements'

    if not _collections_equal(criteria_table.rows, criteria_table.columns):
        raise ValueError('Rows and columns of criteria table must consist of same elements')

    _validate_tables(criteria_table, f'criteria table')

    comparison_items = None

    if len(criteria_comparisons) != len(criteria_table.rows):
        raise ValueError(
            'Criteria comparisons must contain as many pieces of criteria as there are in the criteria table'
        )

    for i in range(len(criteria_comparisons)):
        criteria = criteria_comparisons[i]

        if not _collections_equal(criteria.rows, criteria.columns):
            raise ValueError(criteria_comparison_rows_columns)

        if comparison_items is None:
            comparison_items = criteria.rows
        elif not _collections_equal(comparison_items, criteria.rows):
            raise ValueError(criteria_comparison_rows_columns)

        _validate_tables(criteria, f'criteria_comparison[{i}]')

        if criteria.name not in criteria_table.rows:
            raise ValueError(f'Criteria with name {criteria.name} does not exist in the criteria table')
