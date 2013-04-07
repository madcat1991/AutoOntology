#coding: utf-8
import math


def get_vector(matrix):
    matrix_len = len(matrix)
    vector = []
    for i in range(matrix_len):
        for j in range(i + 1, matrix_len):
            vector.append(matrix[i][j])
    return vector


def get_m(vector):
    res = 0
    vector_len = len(vector)
    for i in range(vector_len):
        res += vector[i]
    return res / vector_len


def get_sigma(vector, mx):
    res = 0
    vector_len = len(vector)
    for i in range(vector_len):
        res += (vector[i] - mx) * (vector[i] - mx)
    return math.sqrt(res)


def get_cov_x_y(x, y, mx, my):
    res = 0
    length = len(x)
    for i in range(length):
        res += (x[i] - mx) * (y[i] - my)
    return res


def get_cophenetic_correlation_coefficient(matrix1, matrix2):
    x = get_vector(matrix1)
    y = get_vector(matrix2)

    mx = get_m(x)
    my = get_m(y)
    sigma_x = get_sigma(x, mx)
    sigma_y = get_sigma(y, my)
    cov_xy = get_cov_x_y(x, y, mx, my)
    return cov_xy / sigma_x / sigma_y
