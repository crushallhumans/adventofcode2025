# adventofcode 2025
# crushallhumans
# puzzle 3
# 12/03/2025

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
TEST_INPUT_STRING_ONE = """987654321111111
811111111111119
234234234234278
818181911112111"""
TEST_INPUT_STRING_TWO = TEST_INPUT_STRING_ONE
TEST_ONE_RESULT = 357
TEST_TWO_RESULT = 3121910778619


def reprocess_input(param_set):
    if isinstance(param_set,str):
        l = []
        l = [input_line.strip() for input_line in param_set.splitlines()]
        param_set = l
    return param_set    


def one_star(param_set, is_two_star = False):
    if not is_two_star: print("---------------one_star--------------------")
    param_set = reprocess_input(param_set)
    r = 0
    highest = [0,0]
    for i in param_set:
        P(i)
        # pass 1
        highest = [(0,0),(0,0)]
        for c,j in enumerate(i):
            jj = int(j)
            if jj > highest[0][0]:
                if c == 0 or c == len(i)-1:
                    highest[1] = highest[0]
                else:
                    highest[1] = (0,0)

                highest[0] = (jj,c)
            elif jj > highest[1][0]:
                highest[1] = (jj,c)            
        highest_sorted = sorted(highest, key = lambda x: x[1])        
        P(highest_sorted)
        val = int(str(highest_sorted[0][0]) + '' + str(highest_sorted[1][0]))
        P(val)
        r += val
    return r

# understanding gained from spieglt! was entirely down a wrong rabbithole
def highest_number(num: str, offset):
    digits = list(num)
    for i in [9,8,7,6,5,4,3,2,1,0]:
        try:
            return str(i), digits.index(str(i)) + offset
        except:
            continue
    return None
def two_star(param_set):
    print("---------------two_star--------------------")
    #return one_star(param_set,True)
    param_set = reprocess_input(param_set)
    r = 0
    for line in param_set:
        P(line)
        digits = []
        last_idx = -1
        for i in range(12):
            end = -(11 - i)
            if end == 0:
                end = None
            next_digit, last_idx = highest_number(line[last_idx + 1:end], last_idx + 1)
            P(last_idx)
            digits.append(next_digit)
        num = int(''.join(digits))
        P(num)
        r += num
    return r



def two_star__rabbithole_nonfunctional(param_set):
    print("---------------two_star--------------------")
    #return one_star(param_set,True)
    param_set = reprocess_input(param_set)
    r = 0
    highest = [0,0]
    for i in param_set:
        P(i)
        ii = str(i)
        ilen = len(ii)
        numlen = 12
        highest = []
        leftmost_highest = 0
        leftmost_position = -1
        for c,jj in enumerate(ii):
            j = int(jj)
            if j > leftmost_highest:
                leftmost_highest = j
                leftmost_position = c
                if j == 9:
                    break
        c = leftmost_position
        while c < ilen:
            hc = int(ii[c])
            if len(highest) < numlen:
                highest.append(hc)
                
            c += 1
        if len(highest) != numlen:
            c = leftmost_position - 1
            while c >= 0:
                hc = int(ii[c])
                if len(highest) < numlen:
                    highest.insert(0,hc)
                else:
                    if hc > highest[0]:
                        highest.pop(0)
                        highest.insert(0,hc)
                    elif hc == highest[0]:
                        P('going in left',c,leftmost_position)
                        d = c
                        while d < leftmost_position-1 and d < numlen:
                            P(d,hc,highest[d])
                            if hc > highest[d]:
                                highest.pop(d)
                                highest.insert(0,hc)
                                break
                            d += 1
            
                c -= 1

        if len(highest) < numlen:
            P(i,highest,force = True)
            exit()
        val = int(''.join([str(i) for i in highest]))
        P(val)
        r += val

        continue


        kk = [(c,j) for c,j in enumerate(str(i))]
        P(kk)
        k = sorted(kk, key = lambda x: ((-1* x[1]),x[0]))
        P(' '.join([str(c[1]).ljust(2) for c in k]))
        P(' '.join([str(c[0]).ljust(2) for c in k]))

        digit_hash = {}
        for c,j in enumerate(str(i)):
            if j not in digit_hash:
                digit_hash[j] = []
            digit_hash[j].append(c)
        for j in digit_hash:
            digit_hash[j] = sorted(digit_hash[j])
        P(digit_hash)



        # pass 1
        highest = [(0,0),(0,0)]
        for c,j in enumerate(i):
            jj = int(j)
            if jj > highest[0][0]:
                if c == 0 or c == len(i)-1:
                    highest[1] = highest[0]
                else:
                    highest[1] = (0,0)

                highest[0] = (jj,c)
            elif jj > highest[1][0]:
                highest[1] = (jj,c)            
        highest_sorted = sorted(highest, key = lambda x: x[1])        
        P(highest_sorted)
        val = int(str(highest_sorted[0][0]) + '' + str(highest_sorted[1][0]))
        P(val)
        r += val
    return r









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
        DEBUG = True

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