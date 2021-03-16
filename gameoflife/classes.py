#!/usr/bin/python3

import pygame
from pygame.locals import *
import numpy as np
import time

'''
Game of life class
'''


class Game:

    cell_size = 10

    def __init__(self, bk='WHITE', cl='BLACK', screen=(700, 700)):
        self.size = screen
        self.background = bk
        self.cellcolor = cl
        self.car = int(screen[0] / self.cell_size)
        self.margin = 1
        self.pause = False
        self.auto = [[0, 0, 1]]

    def start(self):
        c_size = self.cell_size
        screen = pygame.display.set_mode(self.size)
        screen.fill(self.background)
        pygame.display.update()
        running = True
        speed = .5

        n_step = np.zeros((self.car, self.car))

        while running:

            screen.fill(self.background)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == MOUSEBUTTONDOWN:
                    co = event.pos
                    cx, cy = co[1], co[0]
                    px = int(cx / c_size)
                    py = int(cy / c_size)
                    s = self.car
                    if n_step[py, px]:
                        n_step[py, px] = 0
                        pygame.draw.rect(screen, self.cellcolor,
                                         (py * c_size, px * c_size,
                                          c_size, c_size), 1)
                    else:
                        for i in self.auto:
                            n_step[(py + i[0]) % s,
                                   (px + i[1]) % s] = i[2]
                            pygame.draw.rect(screen, self.cellcolor,
                                             ((py + i[0]) * c_size,
                                              (px + i[1]) * c_size,
                                              c_size, c_size))
                    self.pause = True
                    self.draw(n_step, screen)
                elif event.type == KEYDOWN:
                    if event.key == K_p:
                        if self.pause:
                            self.pause = False
                        else:
                            self.pause = True
                    if event.key == K_m:
                        if self.margin:
                            self.margin = 0
                        else:
                            self.margin = 1
                        if self.pause:
                            p = 0
                        else:
                            p = 1
                        self.pause = True
                        screen.fill(self.background)
                        self.draw(n_step, screen)
                        if p:
                            self.pause = False
                            screen.fill(self.background)
                    if event.key == K_LEFT:
                        if speed < 2:
                            speed += .1
                    if event.key == K_RIGHT:
                        if speed > .1:
                            speed -= .1
                    if event.key == K_0:
                        self.auto = [[0, 0, 1]]

                    if event.key == K_1:
                        self.auto = [[0, -1, 1],
                                     [1, 0, 1],
                                     [-1, 1, 1],
                                     [0, 1, 1],
                                     [1, 1, 1]]
                    if event.key == K_2:
                        self.auto = [[-1, -1, 1],
                                     [0, -1, 1],
                                     [1, -1, 1],
                                     [2, -1, 1],
                                     [-2, 0, 1],
                                     [2, 0, 1],
                                     [2, 1, 1],
                                     [-2, 2, 1],
                                     [1, 2, 1]]

            if not self.pause:
                self.draw(n_step, screen)
                time.sleep(speed)
        pygame.quit()

    def draw(self, n_step, screen):

        p_step = n_step.copy()
        s = self.car

        for y in range(0, s):
            for x in range(0, s):
                if not self.pause:
                    n_alive = p_step[(y - 1) % s, (x - 1) % s] + \
                              p_step[(y - 1) % s, x % s] + \
                              p_step[(y - 1) % s, (x + 1) % s] + \
                              p_step[y % s, (x - 1) % s] + \
                              p_step[y % s, (x + 1) % s] + \
                              p_step[(y + 1) % s, (x - 1) % s] + \
                              p_step[(y + 1) % s, x % s] + \
                              p_step[(y + 1) % s, (x + 1) % s]
                    if n_alive == 3:
                        n_step[y, x] = 1
                    elif n_alive > 3 or n_alive < 2:
                        n_step[y, x] = 0
                if n_step[y, x]:
                    pygame.draw.rect(screen, self.cellcolor,
                                     (y * 10, x * 10, 10, 10))
                elif self.margin:
                    pygame.draw.rect(screen, self.cellcolor,
                                     (y * 10, x * 10, 10, 10), 1)
        pygame.display.update()
