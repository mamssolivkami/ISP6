import numpy as np

from hierarchy import *
from data import get_criteria_table, get_alternatives_comparisons, ALTERNATIVES


def _is_iterable(obj):
    try:
        iter(obj)
    except TypeError as te:
        return False

    return True


def _stringify_table_row(row_name, values, row_name_len, values_len):
    row = [str(val).rjust(values_len, ' ') for val in values]
    row = [row_name.rjust(row_name_len, ' ')] + row

    row = '|'.join(row)

    return row


def form_title(title_text):
    pattern = '='
    title_size = 80

    pattern_right = (title_size - len(title_text)) // 2 - 1
    pattern_left = title_size - len(title_text) - pattern_right - 1

    return f'{pattern * pattern_left} {title_text} {pattern * pattern_right}'


def print_table(table: MatrixTable, round_precision=2):
    name = table.name

    cols_len = max(len(col) for col in table.columns)
    rows_len = max(len(row) for row in list(table.rows) + ([] if name is None else [name]))

    print(_stringify_table_row('' if name is None else name, table.columns, rows_len, cols_len))

    for row in table.rows:
        values = []

        for col in table.columns:
            value = table[row, col]

            if isinstance(value, float):
                value = round(value, round_precision)
            elif value is None:
                value = ''

            values.append(value)

        print(_stringify_table_row(row, values, rows_len, cols_len))


def expand_table(table: MatrixTable | None, rows: dict, columns: dict, result_table_name):
    result_rows = [] if table is None else list(table.rows) + list(rows.keys())
    result_cols = [] if table is None else list(table.columns) + list(columns.keys())

    constructed_table = np.full([len(result_rows), len(result_cols)], None)
    constructed_table = MatrixTable(result_rows, result_cols, constructed_table, result_table_name)

    for row in result_rows:
        for col in result_cols:
            value = None

            if table is not None and row in table.rows and col in table.columns:
                value = table[row, col]

            elif row in rows.keys():
                if _is_iterable(rows[row]) and col in rows[row]:
                    value = rows[row][col]
                elif constructed_table.columns.index(col) == 0:
                    value = rows[row]

            elif col in columns.keys():
                if _is_iterable(columns[col]) and row in columns[col]:
                    value = columns[col][row]
                elif constructed_table.rows.index(row) == 0:
                    value = columns[col]

            constructed_table[row, col] = value

    return constructed_table


def table_analysis_to_table(analysis: TableAnalysis, name=None):
    columns = {
        'Ср. геом': analysis.geometric_averages_by_row
    }
    rows = {
        'Сумм.': analysis.sums_by_column,
        'Ср. геом': analysis.geometric_averages_by_row,
        'Норм.': analysis.norm_vector,

        'K': analysis.k,
        'Инд. согл.': analysis.accordance_index,
        'Отнош.': analysis.accordance_ratio
    }

    return expand_table(analysis.table, rows, columns, name)


def full_analysis_to_table(analysis: Analysis, name=None):
    rows = {
        'Норм.': analysis.criteria_norm_vector,
        'Инд. согл.': analysis.accordance_indices,
        'Общ. инд. согл.': analysis.general_accordance_index,
        'Общ. Отнош.': analysis.general_accordance_ratio
    }
    columns = {
        'Приоритет': analysis.priorities
    }

    return expand_table(analysis.table, rows, columns, name)


def main():
    criteria_comparisons = get_criteria_table()
    print(form_title('Критерии'))
    print_table(criteria_comparisons, 3)
    print('\n' + form_title('Сравнения альтернатив'))

    alternatives = ALTERNATIVES
    alternatives_comparisons = get_alternatives_comparisons()
    for table in alternatives_comparisons.values():
        print_table(table)
        print()

    criteria_comparisons = analyze_table(criteria_comparisons)
    alternatives_comparisons = dict((criteria, analyze_table(table)) for criteria, table in alternatives_comparisons.items())

    print('\n' + form_title('Анализ критериев'))
    print_table(table_analysis_to_table(criteria_comparisons), 3)

    print('\n' + form_title('Анализ сравнения альтернатив по критериям'))
    for alt, table in alternatives_comparisons.items():
        print_table(table_analysis_to_table(table, alt), 3)
        print()

    result = analyze_all(alternatives, criteria_comparisons, alternatives_comparisons)
    print_table(full_analysis_to_table(result), 5)


if __name__ == '__main__':
    main()
