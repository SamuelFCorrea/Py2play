#!/usr/bin/python3

import pygame
from pygame.locals import *
import numpy as np
import time

'''
Game of life class
'''


class Game:
    '''
    Atributes:

        size - screen width and heigth.
        background - background color.
        cellcolor - cell color.
        car - columns and rows.
        cell_size - cell size.
        margin - grid in the game.
        pause - game state.
        auto - the auto var is a 2d matrix with the info to fill
               a cell each vector reprecent a cell to change:
               [a, b, c] = a (y coordinate)
                           b (x coordinate)
                           c (cell state 0 or 1)

    Methods:

        start - main fuction, open the window and read the comands.
        draw - draw the matrix.
    '''


    def __init__(self, bk='WHITE', cl='BLACK', screen=(700, 700), cs = 10):
        '''
        Initialize the variables.
        '''
        self.size = screen
        self.background = bk
        self.cellcolor = cl
        self.cell_size = cs
        self.car = int(screen[0] / cs)
        self.margin = True
        self.pause = False
        self.auto = [[0, 0, 1]]

    def start(self):
        '''
        Main fuction, open the window and read the comands.

        c_size - cell size.
        screen - screen object.
        running - variable to keep the bucle open until the user close
                  the window.
        speed - game actualization.
        '''
        c_size = self.cell_size
        screen = pygame.display.set_mode(self.size)
        screen.fill(self.background)
        pygame.display.update()
        running = True
        speed = .5

        '''Matrix initialization'''
        n_step = np.zeros((self.car, self.car))

        while running:
            '''
            Fill the screen with the background color and
            refreshing it.
            '''
            screen.fill(self.background)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    '''If the user quits the game end the bucle'''
                    running = False
                elif event.type == MOUSEBUTTONDOWN:
                    '''
                    On click draw the figure or change the cell status.
                    co - click coordinates.
                    px / py - respective cell column and row.
                    s - varible to store the number of rows and columns.
                    '''
                    co = event.pos
                    cx, cy = co[1], co[0]
                    px = int(cx / c_size)
                    py = int(cy / c_size)
                    s = self.car
                    if n_step[py, px]:
                        '''Kill the cell'''
                        n_step[py, px] = 0
                        pygame.draw.rect(screen, self.cellcolor,
                                         (py * c_size, px * c_size,
                                          c_size, c_size), 1)
                    else:
                        '''Draw the figure'''
                        for i in self.auto:
                            n_step[(py + i[1]) % s,
                                   (px + i[0]) % s] = i[2]
                            pygame.draw.rect(screen, self.cellcolor,
                                             ((py + i[1]) * c_size,
                                              (px + i[0]) * c_size,
                                              c_size, c_size))
                    '''
                    Pause the game to avoid the next step when the user
                    do something, and allow it to continue drawing.
                    '''
                    self.pause = True
                    self.draw(n_step, screen)
                elif event.type == KEYDOWN:
                    '''Key events'''
                    if event.key == K_p:
                        '''The 'p' pause and reanude the game'''
                        if self.pause:
                            self.pause = False
                        else:
                            self.pause = True
                    if event.key == K_m:
                        '''The 'm' removes or draw the grid'''
                        if self.margin:
                            self.margin = False
                        else:
                            self.margin = True
                        '''
                        To avoid lag perseption the grid change can appear
                        in the middle of a step.
                        if the game is in pause before the 'm' is clicked
                        the game must continue in pause.
                        '''
                        if self.pause:
                            p = 0
                        else:
                            p = 1
                        '''Pause the game to avoid the next step'''
                        self.pause = True
                        '''clean the window and draw it again'''
                        screen.fill(self.background)
                        self.draw(n_step, screen)
                        if p:
                            self.pause = False
                            screen.fill(self.background)
                    if event.key == K_LEFT:
                        '''The arrows change the actualization time'''
                        if speed < 2:
                            speed += .1
                    if event.key == K_RIGHT:
                        if speed > .1:
                            speed -= .1
                    if event.key == K_0:
                        '''The number 0 is to modify only one cell'''
                        self.auto = [[0, 0, 1]]
                    if event.key == K_1:
                        '''The number 1 draw a glider'''
                        self.auto = [[-1, 0, 1],
                                     [0, 1, 1],
                                     [1, -1, 1],
                                     [1, 0, 1],
                                     [1, 1, 1]]
                    if event.key == K_2:
                        '''Draw the LWSS'''
                        self.auto = [[-1, -1, 1],
                                     [-1, 0, 1],
                                     [-1, 1, 1],
                                     [-1, 2, 1],
                                     [0, -2, 1],
                                     [0, 2, 1],
                                     [1, 2, 1],
                                     [2, -2, 1],
                                     [2, 1, 1]]
                    if event.key == K_3:
                        '''Draw some thing'''
                        self.auto = [[-1, -2, 1],
                                     [-1, 2, 1],
                                     [0, -1, 1],
                                     [0, -2, 1],
                                     [0, 1, 1],
                                     [0, 2, 1],
                                     [1, -2, 1],
                                     [1, 2, 1]]
                    if event.key == K_c:
                        '''Clean the field'''
                        n_step = np.zeros(self.size)
                        screen.fill(self.background)
                        if self.pause:
                            self.draw(n_step, screen)

            if not self.pause:
                '''If the game is in pause do not pass to the next step'''
                self.draw(n_step, screen)
                time.sleep(speed)
        pygame.quit()

    def draw(self, n_step, screen):
        '''Draw all and aply the game rules'''

        p_step = n_step.copy()
        s = self.car
        cs = self.cell_size

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
                                     (y * cs, x * cs, cs, cs))
                elif self.margin:
                    pygame.draw.rect(screen, self.cellcolor,
                                     (y * cs, x * cs, cs, cs), 1)
        pygame.display.update()
