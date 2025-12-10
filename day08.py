# adventofcode 2025
# crushallhumans
# puzzle 8
# 12/08/2025

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
import heapq
from functools import reduce
from functools import cache
from itertools import chain
from itertools import combinations
from operator import mul
from multiprocessing import Pool
pp = pprint.PrettyPrinter()

ADVENT_YEAR = '2025'
DEBUG = False
TEST_INPUT_STRING_ONE = """162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689"""
TEST_INPUT_STRING_TWO = TEST_INPUT_STRING_ONE
TEST_ONE_RESULT = 40
TEST_TWO_RESULT = 25272


def reprocess_input(param_set):
    if isinstance(param_set,str):
        param_set = sorted(tuple(map(int, n.split(','))) for n in param_set.splitlines())
    return param_set    


# this is again all karanlyons - teaching me python fundamentals I didn't know I lacked
def one_star(param_set, space = 1000, is_two_star = False):
    if not is_two_star: print("---------------one_star--------------------")
    param_set = reprocess_input(param_set)
    c = 0

    circuits = {c: {c} for c in param_set}
    if is_two_star:
        heap = []
        for p in combinations(param_set, 2):
            new_tup = (math.dist(p[0],p[1]), p)
            P('new_tup',new_tup)
            heap.append(new_tup)
        heapq.heapify(heap)
        while heap:
            n = heapq.heappop(heap)
            #_, (a,b) = heapq.heappop(heap)  ### !!! tuple comprehension of *ret ???
            a = n[1][0]
            b = n[1][1]
            if circuits[a] is circuits[b]:
                continue
            circuits[a] |= circuits[b]
            if len(circuits[a]) == len(param_set):
                return a[0] * b[0]
            for c in circuits[b]: circuits[c] = circuits[a]

    else:
        P(circuits)
        P('here we go')
        combos = combinations(param_set, 2)
        combo_heap = heapq.nsmallest(space, combos, key=lambda p: math.dist(*p))
        for a, b in combo_heap:
            P(a,b)
            if circuits[a] is circuits[b]:
                continue
            circuits[a] |= circuits[b]
            for c in circuits[b]:
                circuits[c] = circuits[a]
            P(circuits)

        P(circuits)
        return reduce(mul, heapq.nlargest(3, map(len, {tuple(c) for c in circuits.values()})))


def two_star(param_set):
    print("---------------two_star--------------------")
    return one_star(param_set,is_two_star = True)
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
            one_star(TEST_INPUT_STRING_ONE, space = 10),
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