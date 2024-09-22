import random
import sys
import numpy as np
import pygame
from threading import Thread
from settings import *


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

        self.player_move = True

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
                self.player_move = True

    def draw(self):
        self.screen.fill((0, 0, 0))

        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                if self.matrix[i][j] == 1:
                    pygame.draw.rect(self.screen, (100, 100, 255),
                                     (i * CELL_SIZE, j * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                elif self.matrix[i][j] == 2:
                    pygame.draw.rect(self.screen, (255, 100, 100),
                                     (i * CELL_SIZE, j * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        pygame.display.flip()

    def computer_move(self):
        x = random.randrange(MATRIX_SIZE_X)
        y = random.randrange(MATRIX_SIZE_Y)
        while self.matrix[x][y]:
            x = random.randrange(MATRIX_SIZE_X)
            y = random.randrange(MATRIX_SIZE_Y)
        self.matrix[x][y] = 2

    def exit(self):
        pygame.quit()
        sys.exit()