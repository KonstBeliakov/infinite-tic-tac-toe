import copy
import random
import sys
from functools import lru_cache

import numpy as np
import pygame
from threading import Thread
from settings import *

from utils import evaluation


class Game:
    def __init__(self):
        pygame.init()
        width, height = 800, 600
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Tic-Tac-Toe")

        self.over = False

        self.circle_x = 200
        self.circle_y = 200

        self.circle_radius = 20

        self.matrix = np.array([[0 for _ in range(MATRIX_SIZE_Y)] for _ in range(MATRIX_SIZE_X)])

        self.active = []

        self.font = pygame.font.Font(None, 36)

        self.player_move = True

        self.last_evaluation = 0

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.over = True

            if self.player_move and event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                self.matrix[mouse_x // CELL_SIZE][mouse_y // CELL_SIZE] = 1

                self.player_move = False
                t1 = Thread(target=self.computer_move)
                t1.start()

    def draw(self):
        self.screen.fill((0, 0, 0))

        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                if self.matrix[i][j] == 1:
                    pygame.draw.rect(self.screen, (100, 100, 255),
                                     (i * CELL_SIZE, j * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                elif self.matrix[i][j] == -1:
                    pygame.draw.rect(self.screen, (255, 100, 100),
                                     (i * CELL_SIZE, j * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        text_surface = self.font.render(f'Evaluation: {self.last_evaluation}', True, (255, 255, 255))
        self.screen.blit(text_surface, (50, 100))

        pygame.display.flip()

    def computer_move(self):
        '''x = random.randrange(MATRIX_SIZE_X)
        y = random.randrange(MATRIX_SIZE_Y)
        while self.matrix[x][y]:
            x = random.randrange(MATRIX_SIZE_X)
            y = random.randrange(MATRIX_SIZE_Y)
        self.matrix[x][y] = -1'''

        move, ev = self.min_max(RECURSION_DEPTH, False, ())

        print(move, ev)

        self.matrix[move] = -1
        self.last_evaluation = ev

        self.player_move = True

    def min_max(self, depth, player_move, moves1):  # returns best move and board evaluation
        for move in moves1:
            self.matrix[move[0]][move[1]] = move[2]

        if depth == 0:
            t = evaluation(tuple([tuple(i) for i in self.matrix]))
            for move in moves1:
                self.matrix[move[0]][move[1]] = 0
            return None, t

        moves = set()
        for x in range(1, MATRIX_SIZE_X - 1):
            for y in range(1, MATRIX_SIZE_Y - 1):
                if self.matrix[x][y]:
                    for dx in range(-1, 2, 1):
                        for dy in range(-1, 2, 1):
                            if not self.matrix[x + dx][y + dy]:
                                moves.add((x + dx, y + dy))

        for move in moves1:
            self.matrix[move[0]][move[1]] = 0

        moves_eval = []
        for move in moves:
            color = 1 if player_move else -1
            moves2 = list(copy.deepcopy(moves1)) + [(move[0], move[1], color)]
            _, ev = self.min_max(depth-1, not player_move, moves2)

            moves_eval.append((move, ev))

        if player_move:
            return max(moves_eval, key=lambda x: x[1])
        else:
            return min(moves_eval, key=lambda x: x[1])

    def exit(self):
        pygame.quit()
        sys.exit()