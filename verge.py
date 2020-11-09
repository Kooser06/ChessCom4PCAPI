#!/usr/bin/env pypy
# -*- coding: utf-8 -*-

from itertools import count
from collections import namedtuple

colors = (3, 2, 1, 0)
pvs = (100, 100, 100, 100, 290, 350, 500, 60000)
promotion = [(21, 22, 23, 24, 25, 26, 27, 28), (28, 38, 48, 58, 68, 78, 88, 98), (91, 92, 93, 94, 95, 96, 97, 98), (21, 31, 41, 51, 61, 71, 81, 91)]
directions = [(-10, -11, -9), (1, -9, 11), (10, 11, 9), (-1, -11, 9), (12, 21, -12, -21, 19, -19, 8, -8), (-11, 11, -9, 9), (1, -1, 10, -10), (1, -1, 10, -10, -11, 11, -9, 9)]
valid_keys = (21, 22, 23, 24, 25, 26, 27, 28, 31, 32, 33, 34, 35, 36, 37, 38, 41, 42, 43, 44, 45, 46, 47, 48, 51, 52, 53, 54, 55, 56, 57, 58, 61, 62, 63, 64, 65, 66, 67, 68, 71, 72, 73, 74, 75, 76, 77, 78, 81, 82, 83, 84, 85, 86, 87, 88, 91, 92, 93, 94, 95, 96, 97, 98)
initial = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, (1, 6, 21), (1, 1, 22), 0, 0, (2, 7, 25), (2, 5, 26), (2, 4, 27), (2, 6, 28), 0, 0, (1, 4, 31), (1, 1, 32), 0, 0, (2, 2, 35), (2, 2, 36), (2, 2, 37), (2, 2, 38), 0, 0, (1, 5, 41), (1, 1, 42), 0, 0, 0, 0, 0, 0, 0, 0, (1, 7, 51), (1, 1, 52), 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, (3, 3, 67), (3, 7, 68), 0, 0, 0, 0, 0, 0, 0, 0, (3, 3, 77), (3, 5, 78), 0, 0, (0, 0, 81), (0, 0, 82), (0, 0, 83), (0, 0, 84), 0, 0, (3, 3, 87), (3, 4, 88), 0, 0, (0, 6, 91), (0, 4, 92), (0, 5, 93), (0, 7, 94), 0, 0, (3, 3, 97), (3, 6, 98), 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
pieces = [[1, 6, 21, 0], [1, 4, 31, 0], [1, 5, 41, 0], [1, 7, 51, 0], [1, 1, 22, 0], [1, 1, 32, 0], [1, 1, 42, 0], [1, 1, 52, 0], [2, 7, 25, 0], [2, 5, 26, 0], [2, 4, 27, 0], [2, 6, 28, 0], [2, 2, 35, 0], [2, 2, 36, 0], [2, 2, 37, 0], [2, 2, 38, 0], [0, 0, 81, 0], [0, 0, 82, 0], [0, 0, 83, 0], [0, 0, 84, 0], [0, 6, 91, 0], [0, 4, 92, 0], [0, 5, 93, 0], [0, 7, 94, 0], [3, 3, 67, 0], [3, 7, 68, 0], [3, 3, 77, 0], [3, 5, 78, 0], [3, 3, 87, 0], [3, 4, 88, 0], [3, 3, 97, 0], [3, 6, 98, 0]]

class Position(namedtuple('Position', 'board score turn pieces')):
    def moves(self):
        ret = []
        for piece in self.pieces:
            if piece[0] != self.turn or piece[3] == 1: continue
            for location in directions[piece[1]]:
                for key in count(piece[2] + location, location):
                    if key not in valid_keys: break
                    elif self.board[key] == 0: captured = 0
                    elif self.board[key][0] == self.turn or self.board[key][0] == colors[self.turn]: break
                    else: captured = 1
                    if piece[1] in (0, 1, 2, 3) and location in (-10, 10, 1, -1) and captured == 1: break
                    if piece[1] in (0, 1, 2, 3) and location in (11, -11, 9, -9) and captured == 0: break 
                    ret.append((piece[2], key, captured))
                    if piece[1] in (0, 1, 2, 3, 4, 7): break
        return ret

    def move(self, move):
        val, board, pcs = self.score, self.board[:], self.pieces[:]
        pc_key = self.__get_key(pcs, [self.turn, board[move[0]][1], move[0], 0])
        if move[2] == 1:
            if self.turn in (0, 3): val += pvs[board[move[1]][1]]
            else: val -= pvs[board[move[1]][1]]
        if board[move[0]][1] in (0, 1, 2, 3) and move[1] in promotion[board[move[0]][0]]:
            board[move[0]] = (board[move[0]][0], 6, board[move[0]][2])
            if self.turn in (0, 3): val -= pvs[0] + pvs[6]
            else: val += pvs[0] - pvs[6]
        pcs[pc_key] = [self.turn, board[move[0]][1], move[1], 0]
        if move[2] == 1:
            dead_key = self.__get_key(pcs, [board[move[1]][0], board[move[1]][1], board[move[1]][2], 0])
            pcs[dead_key] = [board[move[1]][0], board[move[1]][1], board[move[1]][2], 1]
        board[move[1]] = (board[move[0]][0], board[move[0]][1], move[1])
        board[move[0]] = 0
        return Position(board, val, (self.turn + 1) % 4, pcs)

    def __get_key(self, array, val):
        for key, value in enumerate(array): 
            if val == value: 
                return key
        return False

    def render(self):
        out = ""
        loop = iter(self.board[:])
        for skip in range(21): next(loop)
        print("+-----+-----+-----+-----+-----+-----+-----+-----+\n")
        for rank in range(8):
            for square in range(8):
                next_square = next(loop)
                if next_square == 0: out += "     |"
                else: out += " " + str(next_square[0]) + "." + str(next_square[1]) + " |"
            for skip_again in range(2): next(loop)
            print("|" + out + "\n")
            print("+-----+-----+-----+-----+-----+-----+-----+-----+\n")
            out = ""

class Searcher:
    def __init__(self):
        self.history = set()
        self.nodes = 0

    def bound(self, position, depth, history = ()):
        self.nodes = 0
        positive_team = (position.turn in (0, 3))
        if positive_team: best_val = 99999
        else: best_val = -99999
        best_move = []
        for move in position.moves():
            new_val = self.search(position.move(move), -100000, 100000, depth - 1);
            if (positive_team and new_val < best_val) or (not positive_team and new_val > best_val):
                best_move = move
                best_val = new_val
        return [best_move, self.nodes]

    def search(self, position, alpha, beta, depth):
        self.nodes += 1
        if depth == 0: return -position.score
        if position.turn in (0, 3):
            best = 99999
            for move in position.moves():
                best = min(best, self.search(position.move(move), alpha, beta, depth - 1))
                beta = min(beta, best)
                if beta <= alpha: return best
        else:
            best = -99999;
            for move in position.moves():
                best = max(best, self.search(position.move(move), alpha, beta, depth - 1))
                alpha = max(alpha, best)
                if beta <= alpha: return best
        return best
