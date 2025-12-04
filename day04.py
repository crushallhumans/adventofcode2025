# adventofcode 2025
# crushallhumans
# puzzle N
# 12/n/2025

import os
import re
import sys
import math
import unittest
import socket
import hashlib
import pprint
import random
import time
from functools import reduce
from functools import cache
from itertools import chain
from multiprocessing import Pool
pp = pprint.PrettyPrinter()

ADVENT_YEAR = '2025'
DEBUG = False
TEST_INPUT_STRING_ONE = """..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@."""
TEST_INPUT_STRING_TWO = TEST_INPUT_STRING_ONE
TEST_ONE_RESULT = 13
TEST_TWO_RESULT = 43

# Define color codes
RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
RESET = '\033[0m' # Resets to default color and style


class SafeGrid:
    def __init__(self, grid_arr, gridstr):
        width = 0
        height = 0
        grid = {}
        free = {}
        blocked = {}
        for y,i in enumerate(grid_arr):
            for x,j in enumerate(i):
                grid[(x,y)] = j
                if j == '@':
                    blocked[(x,y)] = j
                elif j == '.':
                    free[(x,y)] = j
                if x > height:
                    width = x
            if y > height:
                height = y

        self.grid = grid
        self.free = free
        self.blocked = blocked
        self.width = width
        self.height = height
        self.gridstr = gridstr
        P(gridstr)
        P(width,height)
        P()

    def gd(self,x,y):
        if (x,y) in self.grid:
            if self.grid[(x,y)] == '@':
                return 1
        return 0
    
    def highlight(self,highlights,colors = [],neighbors = {}):
        r = ''
        for y in range(self.height+1):
            for x in range(self.width+1):
                if (x,y) in highlights or (x,y) in colors:
                    color = RED if (x,y) in highlights else GREEN
                    xx = neighbors[(x,y)] if (x,y) in neighbors else self.grid[(x,y)]
                    r += f'{color}{xx}{RESET}'
                elif (x,y) in self.grid:
                    r += f'{self.grid[(x,y)]}'
            r += "\n"
        return(r)
    
    def remove_from_grid(self,removers):
        for i in removers:
            if i in self.grid:
                self.grid[i] = '.'
                self.free[i] = '.'
            if i in self.blocked:
                del(self.blocked[i])

def reprocess_input(param_set):
    if isinstance(param_set,str):
        l = []
        l = [input_line.strip() for input_line in param_set.splitlines()]
        return SafeGrid(l,param_set)


def one_star(param_set_raw, is_two_star = False):
    if not is_two_star: print("---------------one_star--------------------")
    s = reprocess_input(param_set_raw) if type(param_set_raw) is not SafeGrid else param_set_raw
    c = 0

    any_removed = 1
    step = 1
    while any_removed >= 1:
        P(f'step: {step}')
        movable = []

        inner_step = 1
        for (k,v) in s.blocked.items():

            if DEBUG and not is_two_star and inner_step > 1:
                time.sleep(.05)
                P('\033[F' * (s.height+4))

            x = k[0]
            y = k[1]
            neighbors = 0

            if v == '@':
                neighbors = (
                    s.gd(x - 1, y - 1)  + s.gd(x - 0, y - 1)   + s.gd(x + 1, y - 1) +
                    s.gd(x - 1, y - 0)  + 0                    + s.gd(x + 1, y - 0) +
                    s.gd(x - 1, y + 1)  + s.gd(x - 0, y + 1)   + s.gd(x + 1, y + 1)
                )
                if neighbors < 4:
                    c += 1
                    movable.append((x,y))

            if DEBUG and not is_two_star:
                P(c)
                P(s.highlight([(x,y)],neighbors = {(x,y): neighbors}))

            inner_step += 1

        P(s.highlight([],colors=movable))

        if is_two_star:
            any_removed = len(movable)
            s.remove_from_grid(movable)
        else:
            any_removed = 0

        step += 1
    return c

def two_star(param_set):
    print("---------------two_star--------------------")
    return one_star(param_set,True)
    param_set = reprocess_input(param_set)
    c = 7777
    for i in param_set:
        continue
    return c









#---------------------------------------------------------
def P(*args, force = False, end = "\n"):
    if DEBUG or force:
        if not len([*args]):
            print('')
        else:
            if len([*args]) > 1:
                if end:
                    print(' '.join(str(x) for x in [*args]),end = end)
                else:
                    pp.pprint([*args])
            else:
                print([*args][0],end = end)


class testCase(unittest.TestCase):
    global DEBUG
    DEBUG = True

    def test_one_star(self):
        self.assertEqual(
            one_star(TEST_INPUT_STRING_ONE),
            TEST_ONE_RESULT
        )

    def test_two_star(self):
        self.assertEqual(
            two_star(TEST_INPUT_STRING_TWO),
            TEST_TWO_RESULT
        )



if __name__ == '__main__':
    try:
        sys.argv[1]
        DEBUG = False

        username = 'crushing'
        m = hashlib.sha256()
        hostname = socket.gethostname()
        m.update(hostname.encode('utf8'))
        if m.hexdigest() == 'ec7c98e2b47378ec88e1f9cce8d6ed91b9d616787c8a37023fd5c67cef1ff71f':
            username = 'conrad.rushing'
        print ('hostname str :',hostname)
        print ('hostname hash:', m.hexdigest())

        filename_script = os.path.basename(__file__)
        print("---------------%s--------------------"%filename_script)
        filename = filename_script.split('.')[0]
        input_set = ()
        
        with open("/Users/%s/Development/crushallhumans/adventofcode_bucket/adventofcode%s/inputs/%s.txt" % (username,ADVENT_YEAR,filename)) as input_file:
            input_set = reprocess_input(input_file.read())

        start = (time.time() * 1000)
        ret = one_star(input_set)
        print (ret)
        print ('elapsed:',(time.time() * 1000) - start,'ms')

        start = (time.time() * 1000)
        ret = two_star(input_set)
        print (ret)
        print ('elapsed:',(time.time() * 1000) - start,'ms')
    except Exception as e:
        print(e)