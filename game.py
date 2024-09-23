import copy
from itertools import chain
from time import perf_counter
import sys
from functools import lru_cache

import numpy as np
import pygame
from threading import Thread
from settings import *

from utils import *


class Game:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Tic-Tac-Toe")

        self.over = False

        self.circle_x = 200
        self.circle_y = 200

        self.circle_radius = 20

        self.matrix = np.array([[0 for _ in range(MATRIX_SIZE_Y)] for _ in range(MATRIX_SIZE_X)])
        self.moves = []

        self.active = []

        self.font = pygame.font.Font(None, 36)

        self.player_move = True

        self.last_evaluation = 0

        self.number_of_moves = 0

        self.textures = [pygame.image.load('O.png'), pygame.image.load('X.png')]

        self.textures[0] = pygame.transform.scale(self.textures[0], (CELL_SIZE, CELL_SIZE))
        self.textures[1] = pygame.transform.scale(self.textures[1], (CELL_SIZE, CELL_SIZE))

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.over = True

            if self.player_move and event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                self.make_move(mouse_x // CELL_SIZE, mouse_y // CELL_SIZE, 1)

                t1 = Thread(target=self.computer_move)
                t1.start()

    def draw_grid(self):
        for i in range(SCREEN_HEIGHT // CELL_SIZE + 1):
            pygame.draw.line(self.screen, (100, 100, 100), (0, i * CELL_SIZE),
                             (SCREEN_WIDTH, i * CELL_SIZE), 1)

        for i in range(SCREEN_WIDTH // CELL_SIZE + 1):
            pygame.draw.line(self.screen, (100, 100, 100), (i * CELL_SIZE, 0),
                             (i * CELL_SIZE, SCREEN_HEIGHT), 1)

    def draw(self):
        self.screen.fill((0, 0, 0))

        self.draw_grid()

        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                if self.matrix[i][j] == 1:
                    self.screen.blit(self.textures[0], (i * CELL_SIZE, j * CELL_SIZE))
                elif self.matrix[i][j] == -1:
                    self.screen.blit(self.textures[1], (i * CELL_SIZE, j * CELL_SIZE))

        text_surface = self.font.render(f'Evaluation: {round(self.last_evaluation, 1)}', True, (255, 255, 255))
        self.screen.blit(text_surface, (50, 100))

        pygame.display.flip()

    def computer_move(self):
        t = perf_counter()
        move, ev = self.min_max(RECURSION_DEPTH, False, (), self.number_of_moves)
        self.last_evaluation = ev

        print(move, ev)
        print(perf_counter() - t)

        self.make_move(*move, -1)

    @lru_cache(None)
    def min_max(self, depth, player_move, moves1, number_of_moves, alpha=float('-inf'), beta=float('inf')):
        for move in moves1:
            self.matrix[move[0]][move[1]] = move[2]

        if depth == 0:
            t = sum([check_game_over(self.matrix, move) for move in moves1])
            for move in moves1:
                self.matrix[move[0]][move[1]] = 0
            return None, t

        for move in moves1:
            c = check_game_over(self.matrix, move)
            if abs(c) >= 100:
                for move in moves1:
                    self.matrix[move[0]][move[1]] = 0
                return None, c

        moves = set()
        for x, y, _ in chain(moves1, self.moves[::-1]):
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    if 0 <= x + dx < MATRIX_SIZE_X and 0 <= y + dy < MATRIX_SIZE_Y and not self.matrix[x + dx][y + dy]:
                        moves.add((x + dx, y + dy))

        for move in moves1:
            self.matrix[move[0]][move[1]] = 0

        moves_eval = []
        for move in moves:
            color = 1 if player_move else -1
            moves2 = list(moves1) + [(move[0], move[1], color)]
            _, ev = self.min_max(depth - 1, not player_move, frozenset(moves2), number_of_moves + 1, alpha, beta)

            moves_eval.append((move, ev))

            # Alpha-beta pruning
            if player_move:
                alpha = max(alpha, ev)
                if beta <= alpha:
                    break
            else:
                beta = min(beta, ev)
                if beta <= alpha:
                    break

        if player_move:
            return max(moves_eval, key=lambda x: x[1])
        return min(moves_eval, key=lambda x: x[1])

    def exit(self):
        pygame.quit()
        sys.exit()

    def make_move(self, x, y, color):
        self.matrix[x][y] = color
        self.moves.append((x, y, 1))
        self.number_of_moves += 1

        self.player_move = not self.player_move
