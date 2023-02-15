import sys
import itertools


class Misc:
    @staticmethod
    def unpack(input_list):
        output_list = []
        for i in input_list:
            if type(i) is list or type(i) is tuple:
                for j in Misc.unpack(i):
                    output_list.append(j)
            else:
                output_list.append(i)
        return output_list

    @staticmethod
    def helloWorld():
        print \
            ("""
inv(input_list) - количество инверсий
scalMul(vector_1, vector_2) - скалярное произведение векторов
tranp(matrix) - транспонирует матрицу
det(matrix) - определитель матрицы
rank(matrix) - ранг матрицы
Matrix(values, num_of_lines, num_of_columns) - создание матрицы, где values - значения матрицы, num_of_lines - число строк, num_of_columns - число столбцов
        """)


class Calc:
    @staticmethod
    def inv(input_list):
        inversions = 0
        for i in range(len(input_list)):
            for j in range(len(input_list) - i - 1):
                if input_list[j] > input_list[j + 1]:
                    input_list[j], input_list[j + 1] = input_list[j + 1], input_list[j]
                    inversions += 1
        return inversions

    @staticmethod
    def scalMul(vector_1, vector_2):
        su = 0
        if len(vector_1) != len(vector_2):
            print("I can't prod these vectors")
            return None
        for i in range(len(vector_1)):
            su += vector_1[i] * vector_2[i]
        return su

    @staticmethod
    def tranp(matrix):
        values = Misc.unpack([matrix.col(i) for i in range(matrix.num_of_columns)])
        return Matrix(values, matrix.num_of_columns, matrix.num_of_lines)

    @staticmethod
    def __minor(matrix, lines, columns):
        lines = sorted(list(lines))
        columns = sorted(list(columns))
        minor = Matrix(range(len(lines) * len(columns)), len(lines), len(columns))
        for i in range(len(lines)):
            for j in range(len(columns)):
                minor[i][j] = matrix[lines[i]][columns[j]]
        return minor

    @staticmethod
    def __algDop(matrix, lines, columns):
        lines = sorted(set(range(matrix.num_of_lines)) - set(lines))
        columns = sorted(set(range(matrix.num_of_columns)) - set(columns))
        minor = Matrix(range(len(lines) * len(columns)), len(lines), len(columns))
        for i in range(len(lines)):
            for j in range(len(columns)):
                minor[i][j] = matrix[lines[i]][columns[j]]
        return minor

    @staticmethod
    def det(matrix):
        if matrix.num_of_columns != matrix.num_of_lines:
            print('Not square matrix')
            sys.exit()
        if matrix.num_of_columns == 1:
            return matrix[0][0]
        else:
            su = 0
            for i in range(matrix.num_of_lines):
                su += matrix[0][i] * Calc.det(Calc.__algDop(matrix, [0], [i])) * (-1 if i % 2 else 1)
            return su

    @staticmethod
    def rank(matrix):
        if matrix.num_of_columns * matrix.num_of_lines == 0:
            return 0, 0
        if matrix.num_of_columns == matrix.num_of_lines and Calc.det(matrix) != 0:
            return matrix, matrix.num_of_columns
        list_of_lines = list(
            itertools.combinations(range(matrix.num_of_lines), max(matrix.num_of_columns, matrix.num_of_lines) - 1))
        list_of_columns = list(
            itertools.combinations(range(matrix.num_of_columns), max(matrix.num_of_columns, matrix.num_of_lines) - 1))
        list_of_minors = []
        for i in list_of_lines:
            for j in list_of_columns:
                minor = Calc.__minor(matrix, i, j)
                if Calc.det(minor) != 0:
                    return minor, minor.num_of_columns
                list_of_minors.append(minor)
        max_rank = (0, 0)
        for i in list_of_minors:
            rank = Calc.rank(i)
            if rank[1] > max_rank[1]:
                max_rank = rank
        return max_rank


class Matrix:
    def __init__(self, values, num_of_lines, num_of_columns=None):
        self.num_of_lines, self.num_of_columns = num_of_lines, num_of_columns or num_of_lines
        self.matrix = [[] for _ in range(self.num_of_lines)]

        if len(values) != self.num_of_lines * self.num_of_columns:
            print('MatrixSizeError')
            sys.exit()

        for i in range(self.num_of_lines):
            for j in range(self.num_of_columns):
                self.matrix[i].append(values[self.num_of_columns * i + j])

    def __str__(self):
        output = str()
        for i in self.matrix:
            for j in i:
                output += str(j) + '\t'
            output += '\n'
        return output + '\n'

    def __getitem__(self, key):
        if isinstance(key, slice):
            return Matrix(Misc.unpack(self.matrix[key.start:key.stop:key.step]),
                          len(self.matrix[key.start:key.stop:key.step]), self.num_of_columns)
        return self.matrix[key]

    def __setitem__(self, key, value):
        self.matrix[key] = value

    def col(self, key):
        return [i[key] for i in self.matrix]

    def line(self, key):
        return self[key]

    def __add__(self, other):
        if isinstance(other, Matrix):
            if self.num_of_lines != other.num_of_lines or self.num_of_columns != other.num_of_columns:
                print('MatAddSizeError')
            matrix = Matrix(range(self.num_of_lines * self.num_of_columns), self.num_of_lines,
                            self.num_of_columns)
            for i in range(self.num_of_lines):
                for j in range(self.num_of_columns):
                    matrix[i][j] = self[i][j] + other[i][j]
            return matrix
        elif isinstance(other, int) or isinstance(other, float):
            matrix = Matrix(range(self.num_of_lines * self.num_of_columns), self.num_of_lines,
                            self.num_of_columns)
            for i in range(self.num_of_lines):
                for j in range(self.num_of_columns):
                    matrix[i][j] = self[i][j] + other
            return matrix

    def __sub__(self, other):
        if isinstance(other, Matrix):
            if self.num_of_lines != other.num_of_lines or self.num_of_columns != other.num_of_columns:
                print('MatAddSizeError')
            matrix = Matrix(range(self.num_of_lines * self.num_of_columns), self.num_of_lines,
                            self.num_of_columns)
            for i in range(self.num_of_lines):
                for j in range(self.num_of_columns):
                    matrix[i][j] = self[i][j] - other[i][j]
            return matrix
        elif isinstance(other, int) or isinstance(other, float):
            matrix = Matrix(range(self.num_of_lines * self.num_of_columns), self.num_of_lines,
                            self.num_of_columns)
            for i in range(self.num_of_lines):
                for j in range(self.num_of_columns):
                    matrix[i][j] = self[i][j] - other
            return matrix

    def __mul__(self, other):
        if isinstance(other, Matrix):
            if self.num_of_columns != other.num_of_lines:
                print("I can't prod this")
                return None
            matrix = Matrix(range(self.num_of_lines * other.num_of_columns), self.num_of_lines,
                            other.num_of_columns)
            for i in range(self.num_of_lines):
                for j in range(other.num_of_columns):
                    matrix[i][j] = Calc.scalMul(self.line(i), other.col(j))
            return matrix
        elif isinstance(other, int) or isinstance(other, float):
            matrix = Matrix(range(self.num_of_lines * self.num_of_columns), self.num_of_lines,
                            self.num_of_columns)
            for i in range(self.num_of_lines):
                for j in range(self.num_of_columns):
                    matrix[i][j] = self[i][j] * other
            return matrix
