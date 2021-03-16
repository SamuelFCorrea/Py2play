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

print('Screen Size (default: 700 x 700) \'only 1 integer number >= 100\':',
      end=' ')
sz = input()
if sz and int(sz) >= 100:
    si = int(sz) - int(sz) % 10
    size = (si, si)
else:
    size = (700, 700)
print('Background Color (default: White):', end=' ')
color = input().upper()
if not color:
    color = 'WHITE'
print('Cell Color (default: Black):', end=' ')
cell = input().upper()
if not cell:
    cell = 'BLACK'

game = Game(color, cell, size)

game.start()
