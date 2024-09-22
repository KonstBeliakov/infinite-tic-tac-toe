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
