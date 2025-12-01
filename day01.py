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
TEST_INPUT_STRING_ONE = """L68
L30
R48
L5
R60
L55
L1
L99
R14
L82"""
TEST_INPUT_STRING_TWO = TEST_INPUT_STRING_ONE
TEST_ONE_RESULT = 3
TEST_TWO_RESULT = 6


def reprocess_input(param_set):
    if isinstance(param_set,str):
        l = []
        l = [input_line.strip() for input_line in param_set.splitlines()]
        param_set = l
    return param_set    


def one_star(param_set, is_two_star = False):
    if not is_two_star: print("---------------one_star--------------------")
    param_set = reprocess_input(param_set)
    c = 0
    d = 0
    dial = 50
    zero_start = False
    z = 0
    for i in param_set:
        P(z,i)
        move = int(i[1:])
        if i[0] == 'L':
            dial -= move
        elif i[0] == 'R':
            dial += move
        
        P(dial)
        passed_thru = False

        dd = 0
        if move > 99:
            P('passes > 1')

        if dial > 99:
            passed_thru = True
            while dial > 99:
                dd += 1
                dial -= 100
        elif dial < 0:
            passed_thru = True
            while dial < 0:
                dd += 1
                dial += 100
        P(dial)

        if passed_thru:
            P('passed_thru')        
        if zero_start:
            P('zero_start')

        if zero_start and passed_thru:
            dd -= 1

        if dial == 0:
            P('points_at_zero')
            zero_start = True
            c += 1
            if is_two_star:
                c += (dd-1 if dd > 0 else 0)
        else:
            zero_start = False
            if is_two_star:
                c += dd
        z += 1

        P(c)
#        P(d)
        P("")
    return c

def two_star(param_set):
    print("---------------two_star--------------------")

    param_set = reprocess_input(param_set)
    c = 0
    dial = 50
    z = 0
    for i in param_set:
        P(z,i)
        move = int(i[1:])
        dir = 1
        if i[0] == 'L':
            dir = -1

        x = 0
        while x < move:
            dial += dir
            P(dial)
            if dial == 0:
                P("\tzero!")
                c += 1
            elif dial > 99:
                P("\tzero!")
                c += 1
                dial -= 100
            elif dial < -99:
                P("\tzero!")
                c += 1
                dial += 100
            x += 1

    return c







#---------------------------------------------------------
def P(*args, force = False, end = False):
    if DEBUG or force:
        if len([*args]) > 1:
            if end:
                print(' '.join(str(x) for x in [*args]),end = end)
            else:
                pp.pprint([*args])
        else:
            if end:
                print(*args,end = end)
            else:
                pp.pprint(*args)


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
        #print (ret)
        print ('elapsed:',(time.time() * 1000) - start,'ms')

        start = (time.time() * 1000)
        ret = two_star(input_set)
        print (ret)
        print ('elapsed:',(time.time() * 1000) - start,'ms')
    except Exception as e:
        print(e)