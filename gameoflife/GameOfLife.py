#!/usr/bin/python3

import pygame
import time
import sys
from classes import Game

'''
The Game of Life, also known simply as Life,
is a cellular automaton devised by the British
mathematician John Horton Conway in 1970.
                                    - 'wikipedia'
'''

print('''
     ____________________________
    |                            |
    |       CONFIGURATIONS       |
    |____________________________|

 ''')

print('Screen Size (default: 700 x 700) \'only 1 integer number >= 100\':')
zi = input()
if zi:
    sz = int(zi) 
    print('Cell Size (default: 10) \'only 1 integer number\':', end=' ')
    ci = input()
    if ci:
        cz = int(ci)
    else:
        cz = 10
    size = (sz, sz)
else:
    size = (700, 700)
    cz = 10

'''The input must be in uppercase'''
print('Background Color (default: White):', end=' ')
color = input().upper()
if not color:
    color = 'WHITE'


print('Cell Color (default: Black):', end=' ')
cell = input().upper()
if not cell:
    cell = 'BLACK'

'''Create the class'''
game = Game(color, cell, size, cz)

'''Start the game'''
game.start()
