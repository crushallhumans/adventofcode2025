# adventofcode 2025
# crushallhumans
# puzzle 7
# 12/07/2025

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

from shapely.geometry import Point as ShapelyPoint
from shapely.geometry import LineString as ShapelyLineString
from shapely.geometry.polygon import Polygon as ShapelyPolygon

from functools import reduce
from functools import cache
from itertools import chain
from multiprocessing import Pool

from collections import Counter
from operator import add, or_



pp = pprint.PrettyPrinter()

ADVENT_YEAR = '2025'
DEBUG = False
TEST_INPUT_STRING_ONE = """.......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
..............."""
TEST_INPUT_STRING_TWO = TEST_INPUT_STRING_ONE
TEST_ONE_RESULT = 21
TEST_TWO_RESULT = 40


class CartesianTheater():
    def __init__(self):
        self.original_string = ''
        self.max_x = 0
        self.max_y = 0
        self.points = {}
        self.rows = []
        self.cols = []
        self.empty_rows = []
        self.empty_cols = []
        self.max_steps = 0
        self.inited = False
        self.start = (0,0)
        self.shapely_points = {}
        self.distances = {}
        self.rays = []
        self.ray_points = {}
        self.impacts = {}
        self.start = ()
        self.cardinal_directions = [
            (0,-1), # N
            (1, 0), # E
            (0, 1), # S
            (-1,0), # W
        ]


    def __str__(self):
        return self.stringify()
    
    def stringify(self, show_paths = False):
        if not self.inited:
            return "need at least one row or point"

        s = ''
        for i in range(0,self.max_y):
            for j in range(0,self.max_x):
                match = (j,i)
                if match in self.ray_points.keys() and match not in self.shapely_points.keys():
                    s += '|'
                else:
                    n = self.points[match]
                    if match not in self.impacts.keys() and match in self.shapely_points.keys():
                        n = '*'
                    s += n
            s += "\n"
        s += "\n"

        s += f"splitters: {len(self.shapely_points.keys())}, impacts: {len(self.impacts.keys())}, rays: {len(self.rays)}\n"
        return s

    def add_row(self,i):
        self.rows.append(list(i))
        self.original_string += f"{i}\n"
        if not self.max_x:
            self.max_x = len(list(i))
        self.max_y += 1
        self.inited = True

    def build_cols(self):
        operating_max_x = self.max_x 
        for i in range(0,operating_max_x):
            col = []
            for j in self.rows:
                col.append(j[i])
            self.cols.append(col.copy())
            
    def build_points(self):
        c = 0
        for i in self.cols:
            d = 0
            for j in i:
                self.points[(c,d)] = j
                if j == 'S':
                    self.start = (c,d)
                if j == '^':
                   self.shapely_points[(c,d)] = True #ShapelyPoint(c,d)
                d += 1
            c += 1

    def get_distances(self):
        for i in self.shapely_points.keys():
            for j in self.shapely_points.keys():
                pair = tuple(sorted([i,j]))
                if i != j and pair not in self.distances.keys():
                    ii = self.shapely_points[i]
                    jj = self.shapely_points[j]
                    self.distances[pair] = int(abs(ii.x - jj.x) + abs(ii.y - jj.y))
                    P(pair,ii,jj,self.distances[pair])
 
    def create_ray(self, start):
        xc = start[0]
        if xc >= 0 and xc < len(self.cols):
            ray = [start]
            for c,i in enumerate(self.cols[xc]):
                if c <= start[1]:
                    continue
                yc = c
                coord = (xc,yc)
                pt = self.points[coord]
                if pt == '^':
                    if coord not in self.impacts.keys():
                        self.impacts[coord] = True
                        self.create_ray((xc-1,yc))
                        self.create_ray((xc+1,yc))
                    break
                else:
                    ray.append((xc,yc))
            self.rays.append(ray.copy())
        return True

    def create_rays(self):
        self.create_ray(self.start)
        for i in self.rays:
            for j in i:
                self.ray_points[j] = True


    def sum_coords(self,a,b):
        return tuple(map(sum,zip(a,b)))

    def get_splitters(self):
        return [{x for x, c in enumerate(l) if c == '^'} for l in self.rows if '^' in l]

    # karanlyons again, with the Counter knowledge
    def manyworlds_rays(self):
        lines = self.rows
        beam = Counter({lines[0].index('S'): 1})
        
        P(self.get_splitters())
        P(beam)
        for splitters in self.get_splitters():
            P(splitters)
            beam = reduce(
                add,
                (
                    Counter({x - 1: i, x + 1: i} if x in splitters else {x: i})
                    for x, i in beam.items()
                ),
            )
            P(beam)
        P(beam)
        P(beam.values())
        return sum(beam.values())



def reprocess_input(param_set):
    if isinstance(param_set,str):
        l = []
        l = [input_line.strip() for input_line in param_set.splitlines()]
        param_set = l
    c = CartesianTheater()
    for i in param_set:
        c.add_row(i)
    c.build_cols()
    c.build_points()
    P(c)
    c.create_rays()
    P(c)
    return c


def one_star(param_set, is_two_star = False):
    if not is_two_star: print("---------------one_star--------------------")
    cartesian_theater = reprocess_input(param_set)
    return len(cartesian_theater.impacts.keys())

def two_star(param_set):
    print("---------------two_star--------------------")
    #return one_star(param_set,True)
    cartesian_theater = reprocess_input(param_set)
    return cartesian_theater.manyworlds_rays()










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
            input_set = input_file.read()

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