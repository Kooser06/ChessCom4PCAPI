#!/usr/bin/env pypy
# -*- coding: utf-8 -*-

def indexing(data):
    if data[0] == 0 and data[1] == 0: return 0
    elif data[0] == 0 and data[1] == 4: return 1
    elif data[0] == 0 and data[1] == 5: return 2
    elif data[0] == 0 and data[1] == 6: return 3
    elif data[0] == 0 and data[1] == 7: return 4
    elif data[0] == 1 and data[1] == 1: return 5
    elif data[0] == 1 and data[1] == 4: return 6
    elif data[0] == 1 and data[1] == 5: return 7
    elif data[0] == 1 and data[1] == 6: return 8
    elif data[0] == 1 and data[1] == 7: return 9
    elif data[0] == 2 and data[1] == 2: return 10
    elif data[0] == 2 and data[1] == 4: return 11
    elif data[0] == 2 and data[1] == 5: return 12
    elif data[0] == 2 and data[1] == 6: return 13
    elif data[0] == 2 and data[1] == 7: return 14
    elif data[0] == 3 and data[1] == 3: return 15
    elif data[0] == 3 and data[1] == 4: return 16
    elif data[0] == 3 and data[1] == 5: return 17
    elif data[0] == 3 and data[1] == 6: return 18
    elif data[0] == 3 and data[1] == 7: return 19
    else: return -1
