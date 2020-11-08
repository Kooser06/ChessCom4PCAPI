#!/usr/bin/env pypy
# -*- coding: utf-8 -*-

import math

from itertools import count
from collections import namedtuple

class Position(namedtuple('Position', 'board score turn pieces ep')):
    def moves(self):
        for piece in self.pieces:
            if piece[0] != self.turn: continue
            for location in directions[piece[1]]:
                for key in count(piece[2] + location, location):
                    if key not in valid_keys: break
                    elif self.board[key] == 0: captured = 0
                    elif self.board[key][0] == self.turn or self.board[key][0] == opposite_colors[self.turn]: break
                    else: captured = 1
                    if piece[1] in (0, 1, 2, 3) and location in (-10, -20, 10, 20, 1, -1, 2, -2) and captured == 1: break 
                    if piece[1] in (0, 1, 2, 3) and location in (20, -20, 2, -2) and self.board[key - (location / 2)] != 0: break
                    if piece[1] in (0, 1, 2, 3) and location in (11, -11, 9, -9) and captured == 0: break 
                    yield (piece[2], key, captured)
