# adventofcode 2025
# crushallhumans
# puzzle 2
# 12/02/2025

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
TEST_INPUT_STRING_ONE = """11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124"""
TEST_INPUT_STRING_TWO = TEST_INPUT_STRING_ONE
TEST_ONE_RESULT = 1227775554
TEST_TWO_RESULT = 4174379265


def reprocess_input(param_set):
    if isinstance(param_set,str):
        l = []
        l = [input_line.strip() for input_line in param_set.splitlines()]
        param_set = l[0].split(',')
    return param_set    

def repeater_check(i):
    s = str(i)
    l = len(s)
    if l % 2:
        return False
    d = int(l/2)
    a = s[0:d]
    b = s[d:]
    if (d == 1):
        a = s[0]
        b = s[1]
    if a == b:    
        P(i)
        P(d)
        P(a)
        P(b)
        P('repeater - invalid')        
        return True
    return 0

def repeater_check_two(i):
    s = str(i)
    # INCORRECT - did not properly ignore single-item sets
    # if len(set(list(s))) == 1:
    #     P(i)
    #     P([int(m) for m in list(s)])
    #     P('repeater at layer 1 - invalid')        
    #     return True
    l = len(s)
    d = l//2
    while d > 0:
    # while d > 1: # skip 1 - handled by set comprehension above (except incorrect)
        if l % d:
            d -= 1
            continue
        layer_step = 0
        comparison_list = []
        while layer_step < l:
            a = s[0+layer_step:d+layer_step]
            if not a[0]:
                print(s,d,a,l,layer_step)
                exit()
            comparison_list.append(int(a))
            layer_step += d
        if len(comparison_list) > 1 and len(set(comparison_list)) == 1:
            P(i)
            P(comparison_list)
            P(f'repeater at layer {d} - invalid')    
            return True

        d -= 1

    return False

def one_star(param_set, is_two_star = False):
    if not is_two_star: print("---------------one_star--------------------")
    P(param_set)
    param_set = reprocess_input(param_set)
    c = 0
    for i in param_set:
        range = [int(j) for j in i.split('-')]
        d = range[0]
        P(range)
        while d < range[1]+1:
            x = repeater_check(d) if not is_two_star else repeater_check_two(d)
            if x:
                c += d
                P(c)
                P('----------------')
            d += 1
        P('*****************************')
        P()
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
def P(*args, force = False, end = False):
    if DEBUG or force:
        if not len([*args]):
            print('')
            return None
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
        print (ret)
        print ('elapsed:',(time.time() * 1000) - start,'ms')

        start = (time.time() * 1000)
        ret = two_star(input_set)
        print (ret)
        print ('elapsed:',(time.time() * 1000) - start,'ms')
    except Exception as e:
        print(e)