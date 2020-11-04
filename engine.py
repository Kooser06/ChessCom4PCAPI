#!/usr/bin/env pypy
# -*- coding: utf-8 -*-

import math
from itertools import count
from collections import namedtuple

TABLE_SIZE = 1e7

col = (3, 2, 1, 0)
pvs = (100, 300, 425, 525, 1025, 60000)
pst = [[
    (0, 0, 0, 0, 0, 0, 0, 0, 10, 15, 5, 10, 10, 10, 20, 15, -5, -10, 20, 15, 20, -5, -5, -5, -10, -5, 10, 10, 10, 10, -5, 0, 15, 20, 15, 15, 10, -5, 0, 0, 5, 25, 0, 15, -20, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    (),
    (),
    (),
    ()
], [
    (0, 0, -10, -5, -10, -15, 10, 0, 0, 0, 25, -5, -10, -10, -5, 0, 0, 0, 20, -5, -5, -5, -5, 0, 0, 0, 15, 20, 10, -10, -5, 0, 0, 0, 10, 15, 20, 5, 10, 0, 0, 0, 0, 20, 15, 15, 15, 0, 0, 0, 0, 0, 10, 20, 20, 0, 0, 0, 0, 0, 0, -5, -5, 0),
    (),
    (),
    (),
    ()
], [
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -20, 15, 20, 25, 5, 0, 0, -5, 10, 15, 15, 20, 15, 0, -5, 10, 10, 10, 10, -5, -10, -5, -5, -5, 20, 15, 20, -10, -5, 15, 20, 10, 10, 10, 5, 15, 10, 0, 0, 0, 0, 0, 0, 0, 0),
    (),
    (),
    (),
    ()
], [
    (0, -5, -5, 0, 0, 0, 0, 0, 0, 20, 20, 10, 0, 0, 0, 0, 0, 15, 15, 15, 20, 0, 0, 0, 0, 10, 5, 20, 15, 10, 0, 0, 0, -5, -10, 10, 20, 15, 0, 0, 0, -5, -5, -5, -5, 20, 0, 0, 0, -5, -10, -10, -5, 25, 0, 0, 0, 10, -15, -10, -5, -10, 0, 0),
    (),
    (),
    (),
    ()
]]
con = (50, 35, 30, 10, 4)
mob = ()

class Search:
    def __init__():
        self.tp_score = {}
        self.tp_move = {}
        self.history = set()
        self.nodes = 0

    def search(self, position, history = ()):
        self.nodes = 0
        self.history = set(history)
        for depth in range(1, 1000):
            for move in position.moves():
                val = self.bound(position.move(move), -math.inf, math.inf, depth)
                if val < best and (position.turn == 0 or position.turn == 2): best_move = move
                if val > best and (position.turn == 1 or position.turn == 3): best_move = move
        yield depth, self.tp_move.get(position), self.tp_score.get((position, depth, True)).lower

    def bound(self, position, alpha, beta, depth, root = True):
        self.nodes += 1
        depth = max(depth, 0)
        if not root and position not in self.history: return 0
        if depth == 0: return quiesce(position, alpha, beta)
        for move in position.moves():
            val = -self.bound(position.move(move), -beta, -alpha, depth - 1, False)
            if val >= beta: return beta
            if val > alpha: alpha = val
        if len(self.tp_score) > TABLE_SIZE: self.tp_score.clear()
        return alpha

    def quiesce(self, position, alpha, beta):
        current_score = position.score
        if current_score >= beta: return beta
        if alpha < current_score: alpha = current_score
        for capture in position.captures():
            val = -self.quiesce(position.move(capture), -beta, -alpha)
            if val >= beta: return beta
            if val > alpha: alpha = val
        return alpha
  
