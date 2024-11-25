import numpy as np


class MatrixTable:
    def __init__(self, rows: list | tuple, columns: list | tuple, matrix: np.ndarray=None, name=None):
        self.__rows = tuple(rows)
        self.__columns = tuple(columns)

        shape = (len(rows), len(columns))
        if matrix is None:
            matrix = np.zeros(shape)
        elif matrix.shape != shape:
            raise ValueError('Matrix shape must correspond count of rows and columns')

        self.__matrix = matrix

        self.__name = name

    @property
    def rows(self):
        return self.__rows

    @property
    def columns(self):
        return self.__columns

    @property
    def name(self):
        return self.__name

    @property
    def matrix(self):
        return self.__matrix

    def __get_internal_indices(self, row, column):
        return (self.__rows.index(row), self.__columns.index(column))

    def __getitem__(self, item):
        row, column = item
        row, column = self.__get_internal_indices(row, column)

        return self.__matrix[row, column]

    def __setitem__(self, key, value):
        row, column = key
        row, column = self.__get_internal_indices(row, column)

        self.__matrix[row, column] = value

    def copy(self, new_name=None, names_only=False, leave_name_none=False):
        rows = self.__rows
        columns = self.__columns

        matrix = np.zeros([rows, columns]) if names_only else self.__matrix.copy()

        name = self.__name if new_name is None and not leave_name_none else new_name

        return MatrixTable(rows, columns, matrix, name)

    def apply_function(self, matrix_transformation):
        matrix_transformation(self.__matrix)

    def column_to_dict(self, column_name):
        return dict((row, self[row, column_name]) for row in self.__rows)

    def row_to_dict(self, row_name):
        return dict((col, self[row_name, col]) for col in self.__columns)
