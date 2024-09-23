from functools import lru_cache
from settings import *


@lru_cache(None)
def evaluation(matrix: tuple):
    for x in range(MATRIX_SIZE_X - 4):
        for y in range(MATRIX_SIZE_Y - 4):
            if matrix[x][y]:
                if matrix[x][y] == matrix[x + 1][y] == matrix[x + 2][y] == matrix[x + 3][y] == matrix[x + 4][y]:
                    return matrix[x][y]
                if matrix[x][y] == matrix[x][y + 1] == matrix[x][y + 2] == matrix[x][y + 3] == matrix[x][y + 4]:
                    return matrix[x][y]
                if matrix[x][y] == matrix[x + 1][y + 1] == matrix[x + 2][y + 2] == matrix[x + 3][y + 3] == matrix[x + 4][y + 4]:
                    return matrix[x][y]

    for x in range(MATRIX_SIZE_X - 4):
        for y in range(4, MATRIX_SIZE_Y):
            if matrix[x][y] and matrix[x][y] == matrix[x + 1][y - 1] == matrix[x + 2][y - 2] == matrix[x + 3][y - 3] == matrix[x + 4][y - 4]:
                return matrix[x][y]
    return 0


def check_game_over(matrix, last_move):
    x, y, last_color = last_move

    # checking horizontal
    h1 = 0
    while x + h1 < MATRIX_SIZE_X and matrix[x + h1][y] == last_color:
        h1 += 1
    h2 = 0
    while x - h2 >= 0 and matrix[x - h2][y] == last_color:
        h2 += 1
    if h1 + h2 - 1 >= 5:
        return 1 if last_color == 1 else -1

    # checking vertical
    v1 = 0
    while y + v1 < MATRIX_SIZE_Y and matrix[x][y + v1] == last_color:
        v1 += 1
    v2 = 0
    while y - v2 >= 0 and matrix[x][y - v2] == last_color:
        v2 += 1
    if v1 + v2 - 1 >= 5:
        return 1 if last_color == 1 else -1

    # checking diagonal
    d1 = 0
    while x + d1 < MATRIX_SIZE_X and y + d1 < MATRIX_SIZE_X and matrix[x + d1][y + d1] == last_color:
        d1 += 1
    d2 = 0
    while x - d2 >= 0 and y - d2 >= 0 and matrix[x - d2][y - d2] == last_color:
        d2 += 1
    if d1 + d2 - 1 >= 5:
        return 1 if last_color == 1 else -1

    # checking second diagonal
    d1_2 = 0
    while x + d1_2 < MATRIX_SIZE_X and y - d1_2 >= 0 and matrix[x + d1_2][y - d1_2] == last_color:
        d1_2 += 1
    d2_2 = 0
    while x - d2_2 > 0 and y + d2_2 < MATRIX_SIZE_Y and matrix[x - d2_2][y + d2_2] == last_color:
        d2_2 += 1
    if d1_2 + d2_2 - 1 >= 5:
        return 1 if last_color == 1 else -1
    return 0
