# adventofcode 2025
# crushallhumans
# puzzle 9
# 12/09/2025

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
from shapely.geometry import Polygon as ShapelyPolygon
from shapely.geometry import box as ShapelyBox
from shapely.ops import orient as ShapelyOrient
import shapely as ShapelyAll

from functools import reduce
from functools import cache
from itertools import chain
from itertools import product
from itertools import combinations
from multiprocessing import Pool

from collections import Counter
from operator import add, or_



pp = pprint.PrettyPrinter()

ADVENT_YEAR = '2025'
DEBUG = False
TEST_INPUT_STRING_ONE = """7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3"""
TEST_INPUT_STRING_TWO = TEST_INPUT_STRING_ONE
TEST_ONE_RESULT = 50
TEST_TWO_RESULT = 24


class CartesianTheater():
    def __init__(self):
        self.original_string = ''
        self.max_x = 0
        self.max_y = 0
        self.points = {}
        self.ordered_points = []
        self.points_in_poly = set()
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
                n = '.'
                if match in self.points.keys():
                    n = '#'
                if match in self.points_in_poly:
                    n = '#'
                s += n
            s += "\n"
        s += "\n"

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

    def add_point(self,i):
        x,y = [float(z) for z in i.split(',')]
        P(x,y)
        self.points[(x,y)] = True
        self.ordered_points.append((x,y))
        if not self.max_x or x > self.max_x:
            self.max_x = int(x)
        if not self.max_y or y > self.max_y:
            self.max_y = int(y)
    
    def build_rows_and_cols_from_points(self):
        self.max_x += 2
        self.max_y += 2
        self.rows = [ [] * self.max_x for _ in range(self.max_y) ]
        self.cols = [ [] * self.max_y for _ in range(self.max_x) ]
        self.inited = True

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

    # Get segments using zip and map
    def get_segments(self,ring):
        # curve.coords[:-1] gets all but the last point
        # curve.coords[1:] gets all but the first point
        # zip pairs them up: (p1, p2), (p2, p3), ... (last_p, first_p)
        return [i.length for i in list(map(ShapelyLineString, zip(ring.coords[:-1], ring.coords[1:])))]

    def get_rect_size(self,i):
        x_points = abs(
            max(i[0][0],i[1][0]) - 
            min(i[0][0],i[1][0])
        ) + 1
        y_points = abs(
            max(i[0][1],i[1][1]) - 
            min(i[0][1],i[1][1])
        ) + 1
        return(x_points * y_points)

    def get_all_rectangles(self):
        foo = combinations(self.points.keys(),2)
        pairs = combinations(self.points.keys(),2)
        largest = 0
        nn = len(list(foo))
        nnn = 0
        for i in pairs:
            P(f'{nnn} / {nn}')

            x = self.get_rect_size(i)

            if x > largest:
                largest = x
            nnn += 1
        return largest

    def get_rect_minmax(self,point1,point2):
        x1, y1 = point1
        x2, y2 = point2

        min_x = int(min(x1, x2))
        max_x = int(max(x1, x2))
        min_y = int(min(y1, y2))
        max_y = int(max(y1, y2))
        return (min_x,min_y,max_x,max_y)


    def get_all_points_in_rectangle(self,point1,point2):
        min_x, min_y, max_x, max_y = self.get_rect_minmax(point1,point2)

        # x_coords = range(min_x, max_x + 1)  # +1 to include max_x
        # y_coords = range(min_y, max_y + 1)  # +1 to include max_y
        # # Use itertools.product to get all combinations of x and y

        pts_in_rect = self.get_rect_size((point1,point2))
        P(pts_in_rect)
        return(pts_in_rect,(min_x,min_y,max_x,max_y))


    def get_all_rectangles_within_polygon(self):
        # most_xy = [0,0]
        # least_xy = [int(self.max_x),int(self.max_y)]
        # for ii in self.ordered_points:
        #     i = (int(ii[0]),int(ii[1]))
        #     if i[0] > most_xy[0]:
        #         most_xy[0] = i[0]
        #     if i[1] > most_xy[1]:
        #         most_xy[1] = i[1]
        #     if i[0] < least_xy[0]:
        #         least_xy[0] = i[0]
        #     if i[1] < least_xy[1]:
        #         least_xy[1] = i[1]
        # print(most_xy,least_xy)
        # xlast = 0


        # minx, miny, maxx, maxy = master_polygon.bounds
        # cell_size = 1 # Adjust for desired point density

        # points_inside = []
        # x_coords = [minx + i * cell_size for i in range(int(math.ceil((maxx - minx) / cell_size)) + 1)]
        # y_coords = [miny + i * cell_size for i in range(int(math.ceil((maxy - miny) / cell_size)) + 1)]

        # # need multiprocessing here!
        # # or dumb line counting - for each line segment in polygon, get all points
        # #   scan each line implicated, add areas between point pairs?
        # for x in x_coords:
        #     for y in y_coords:
        #         print(x,y, len(points_inside))
        #         point = ShapelyPoint(x, y)
        #         if master_polygon.contains(point):
        #             points_inside.append((x, y))

        # print(f"Generated points inside: {points_inside}")

        # get all points in poly from shapely
        # go through each and check 9 neighbors, add to set if intersect

        # for x in range(least_xy[0]-1,most_xy[0]+1):
        #     for y in range(least_xy[1]-1,most_xy[1]+1):
        #         if xlast != x:
        #             print(x,y)
        #             xlast = x
        #         P(x,y)
        #         p = ShapelyPoint(x,y)
        #         if master_polygon.contains(p) or p.intersects(master_polygon.boundary):
        #             self.points_in_poly.add((x,y))
        P(self)
        foo = combinations(self.points.keys(),2)
        pairs = combinations(self.points.keys(),2)
        largest = 0
        nn = len(list(foo))
        self.ordered_points.append(self.ordered_points[-1])
        master_polygon = ShapelyPolygon(self.ordered_points)

        nnn = 0
        sized_rectangles = set()
        for i in pairs:
            points_in_rect, maxs = self.get_all_points_in_rectangle(*i)
            P(f'{nnn} / {nn} - pts_in_rect {points_in_rect}')

            sized_rectangles.add((maxs,points_in_rect))
            nnn += 1

        P(sized_rectangles)
        P('resorting rectangles')
        for i in sorted(list(sized_rectangles), key = lambda a: -a[1]):
            maxs = i[0]
            zz = i[1]
            P(i)
            if zz > largest and master_polygon.contains(ShapelyBox(*maxs)):
                P(f'enclosed largest: {zz}' )
                largest = zz
                break

#        points_not_in_poly = set()
            # for j in points_in_rect:
            #     if j not in self.points_in_poly:
            #         points_enclosed = False
            #         break
            # if points_enclosed:
            #     P('enclosed - old')
            #     zz = len(points_in_rect)
            #     if zz > largest:
            #         largest = zz
            # else:
            #     rect_polygon = ShapelyBox(*maxs)
            #     if master_polygon.covers(rect_polygon):
            #         P('enclosed - new')
            #         self.points_in_poly |= points_in_rect
            #         zz = len(points_in_rect)
            #         if zz > largest:
            #             largest = zz
    

#            P(points_in_rect)
#            P(points_in_poly)
            # possibly_subset = True
            # for j in points_in_rect:
            #     print(j)
            #     if j not in self.points_in_poly and j not in points_not_in_poly:
            #         p = ShapelyPoint(j[0],j[1])
            #         if master_polygon.contains(p) or p.intersects(master_polygon.boundary):
            #             self.points_in_poly.add(j)
            #         else:
            #             possibly_subset = False
            #             break
            #     else:
            #         points_not_in_poly.add(j)
            # if possibly_subset:
#            if points_in_rect.issubset(self.points_in_poly):
#                P(len(points_in_rect))
#                P(len(points_in_rect.difference(self.points_in_poly)))

        return largest

    def get_distances(self):
        for i in self.shapely_points.keys():
            for j in self.shapely_points.keys():
                pair = tuple(sorted([i,j]))
                if i != j and pair not in self.distances.keys():
                    ii = self.shapely_points[i]
                    jj = self.shapely_points[j]
                    self.distances[pair] = int(abs(ii.x - jj.x) + abs(ii.y - jj.y))
                    P(pair,ii,jj,self.distances[pair])
 

    def sum_coords(self,a,b):
        return tuple(map(sum,zip(a,b)))

    def get_splitters(self):
        return [{x for x, c in enumerate(l) if c == '^'} for l in self.rows if '^' in l]




def reprocess_input(param_set):
    if isinstance(param_set,str):
        l = []
        l = [input_line.strip() for input_line in param_set.splitlines()]
        param_set = l
    c = CartesianTheater()
    for i in param_set:
        c.add_point(i)
    c.build_rows_and_cols_from_points()
    return c


def one_star(param_set, is_two_star = False):
    if not is_two_star: print("---------------one_star--------------------")
    cartesian_theater = reprocess_input(param_set)
    P(cartesian_theater)
    return(cartesian_theater.get_all_rectangles())

def two_star(param_set):
    print("---------------two_star--------------------")
    #return one_star(param_set,True)
    cartesian_theater = reprocess_input(param_set)
    return cartesian_theater.get_all_rectangles_within_polygon()










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