import sys
import itertools
import time

__all__ = ['Calc', 'Matrix']
print("""
inv(input_list) - количество инверсий
scalMul(vector_1, vector_2) - скалярное произведение векторов
tranp(matrix) - транспонирует матрицу
matrix.det - определитель матрицы
matrix.rank - ранг матрицы
Matrix(values, num_of_lines, num_of_columns) - создание матрицы, 
где values - значения матрицы, num_of_lines - число строк, num_of_columns - число столбцов
        """)


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
    def input_matrix(matrix):
        lines = []
        line = [int(i) for i in input(' ').rstrip().lstrip().split(' ')]
        lines.append(line)
        matrix.num_of_columns = len(lines[0])
        while True:
            line = input(' ').split(' ')
            if line != ['']:
                line = [int(i) for i in line]
            else:
                break
            if len(line) != matrix.num_of_columns:
                print('MatrixSizeError')
                sys.exit()
            lines.append(line)
        matrix.num_of_lines = len(lines)
        matrix.matrix = lines

    @staticmethod
    def is_str(a, b):  # нейросеть понимает текст по русски
        sovpadeniya = 0
        for i in range(min(len(a), len(b))):
            if a[i] == a[i]:
                sovpadeniya += 1

        if sovpadeniya >= 0.8 * len(a):
            return True
        return False

    @staticmethod
    def timer(obj, *args, reps=1):
        if str(type(obj)) == "<class 'function'>":
            start = time.time()
            for i in range(reps):
                obj(*args)
            print(time.time() - start)
            return


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
    def scal_mul(vector_1, vector_2):
        scal_mul = 0
        assert len(vector_1) == len(vector_2), "I can't prod these vectors"
        for i in range(len(vector_1)):
            scal_mul += vector_1[i] * vector_2[i]
        return scal_mul

    @staticmethod
    def transpose(matrix):
        values = Misc.unpack([matrix.col(i) for i in range(matrix.num_of_columns)])
        return Matrix(values, matrix.num_of_columns, matrix.num_of_lines)

    @staticmethod
    def minor(matrix, lines, columns):
        lines = sorted(list(lines))
        columns = sorted(list(columns))
        minor = Matrix(range(len(lines) * len(columns)), len(lines), len(columns))
        for i in range(len(lines)):
            for j in range(len(columns)):
                minor[i][j] = matrix[lines[i]][columns[j]]
        return minor

    @staticmethod
    def alg_dop(matrix, lines, columns):
        lines = sorted(set(range(matrix.num_of_lines)) - set(lines))
        columns = sorted(set(range(matrix.num_of_columns)) - set(columns))
        minor = Matrix(range(len(lines) * len(columns)), len(lines), len(columns))
        for i in range(len(lines)):
            for j in range(len(columns)):
                minor[i][j] = matrix[lines[i]][columns[j]]
        return minor

    @staticmethod
    def det(matrix):
        assert matrix.num_of_columns == matrix.num_of_lines, 'Not square matrix'
        if matrix.num_of_columns == 1:
            return matrix[0][0]
        elif matrix.num_of_columns == 2:
            return matrix[0][0] * matrix[1][1] - matrix[1][0] * matrix[0][1]
        else:
            su = 0
            for i in range(matrix.num_of_lines):
                if matrix[0][i] == 0:
                    continue
                su += matrix[0][i] * Calc.det(Calc.alg_dop(matrix, [0], [i])) * (-1 if i % 2 else 1)
            return su

    @staticmethod
    def rank(matrix, size=1):
        if matrix.num_of_columns * matrix.num_of_lines == 0:
            return 0, 0
        list_of_lines = itertools.combinations(range(matrix.num_of_lines), size)
        list_of_columns = itertools.combinations(range(matrix.num_of_columns), size)
        for i in list_of_lines:
            for j in list_of_columns:
                minor = Calc.minor(matrix, i, j)
                if Calc.det(minor) != 0:
                    rank = Calc.rank(matrix, size + 1)
                    if rank != 0:
                        return rank
                    else:
                        return size, minor
        return 0


class Matrix:
    def __init__(self, values=None, num_of_lines=None, num_of_columns=None):
        if values is None and num_of_lines is None and num_of_columns is None:
            Misc.input_matrix(self)
        else:
            self.num_of_lines, self.num_of_columns = num_of_lines, num_of_columns or num_of_lines
            self.matrix = [[] for _ in range(self.num_of_lines)]

            assert len(values) == self.num_of_lines * self.num_of_columns, 'MatrixSizeError'

            for i in range(self.num_of_lines):
                for j in range(self.num_of_columns):
                    self.matrix[i].append(values[self.num_of_columns * i + j])

    def __str__(self):
        output = ''
        max_len = max([len(str(i)) for i in Misc.unpack(self.matrix)])
        for line in self.matrix:
            for j in line:
                if j >= 0:
                    output += ' ' + str(j) + ' ' * (max_len - len(str(j)))
                else:
                    output += str(j) + ' ' * (1 + max_len - len(str(j)))
            output += '\n'
        return output + '\n\r'

    def __getitem__(self, key):
        if isinstance(key, slice):
            return Matrix(Misc.unpack(self.matrix[key.start:key.stop:key.step]),
                          len(self.matrix[key.start:key.stop:key.step]), self.num_of_columns)
        return self.matrix[key]

    def __setitem__(self, key, value):
        self.matrix[key] = value

    def __getattr__(self, item):
        if item == 'rank':
            self.rank = Calc.rank(self)[0]
            return self.rank
        elif item == 'det':
            if self.rank < self.num_of_columns:
                self.det = 0
                return 0
            else:
                self.det = Calc.det(self)
                return self.det
        elif item == 'tran':
            self.tran = Calc.transpose(self)
            return self.tran

    def __add__(self, other):
        if isinstance(other, Matrix):
            assert self.num_of_lines == other.num_of_lines and self.num_of_columns == other.num_of_columns, 'MatAddSizeError'
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
            assert self.num_of_lines == other.num_of_lines and self.num_of_columns == other.num_of_columns, 'MatAddSizeError'
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
            assert self.num_of_columns == other.num_of_lines, "I can't prod this"
            matrix = Matrix(range(self.num_of_lines * other.num_of_columns), self.num_of_lines,
                            other.num_of_columns)
            for i in range(self.num_of_lines):
                for j in range(other.num_of_columns):
                    matrix[i][j] = Calc.scal_mul(self.line(i), other.col(j))
            return matrix
        elif isinstance(other, int) or isinstance(other, float):
            matrix = Matrix(range(self.num_of_lines * self.num_of_columns), self.num_of_lines,
                            self.num_of_columns)
            for i in range(self.num_of_lines):
                for j in range(self.num_of_columns):
                    matrix[i][j] = self[i][j] * other
            return matrix

    def col(self, key):
        return [i[key] for i in self.matrix]

    def line(self, key):
        return self[key]
