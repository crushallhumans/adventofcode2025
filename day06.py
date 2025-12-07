# adventofcode 2025
# crushallhumans
# puzzle 6
# 12/6/2025

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
TEST_INPUT_STRING_ONE = """123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   +  """
TEST_INPUT_STRING_TWO = TEST_INPUT_STRING_ONE
TEST_ONE_RESULT = 4277556
TEST_TWO_RESULT = 3263827


def reprocess_input(param_set, do_strip = True):
    if isinstance(param_set,str):
        l = []
        if do_strip:
            l = [input_line.strip() for input_line in param_set.splitlines()]
        else:
            l = param_set.splitlines()
        param_set = l
    return param_set


def one_star(param_set, is_two_star = False):
    if not is_two_star: print("---------------one_star--------------------")
    param_set = reprocess_input(param_set)
    columns = []
    for i in param_set:
        ii = re.split('\\s+',i)
        P(ii)
        P(len(ii))
        if not columns:
            columns = [ [] * 1 for _ in range(len(ii)) ]
        P(columns)
        for c,j in enumerate(ii):
            if j != "*" and j != '+':
                columns[c].append(int(j))
            else:
                columns[c].append(j)
    c = 0
    for i in columns:
        P(i)
        op = i.pop()
        if op == '+':
            c += sum(i)
        elif op == '*':
            c += math.prod(i)
    return c


def two_star(param_set):
    print("---------------two_star--------------------")
    #return one_star(param_set,True)
    param_set = reprocess_input(param_set, do_strip = False)
    columns = []
    widths = []
    w = 1
    # get all indices of + or *
    P(param_set[-1])
    pluss = [a.start() for a in list(re.finditer('\\+', param_set[-1]))]
    mults = [a.start() for a in list(re.finditer('\\*', param_set[-1]))]
    op_slices = pluss
    op_slices.extend(mults)
    split_set = set(op_slices)
    split_set.add(0)
    splits = (sorted(list(split_set)))
    slices = []
    for c,i in enumerate(splits):
        if c == len(splits) - 1:
            slices.append((i,None))
        else:
            slices.append((i,splits[c+1]-1))
    P(slices)

    for line in param_set:
        P(line)
        if not columns:
            columns = [ [] * 1 for _ in range(len(pluss)) ]
        for c,i in enumerate(slices):   
            slic = line[i[0]:i[1]]
            P(i,slic) 
            columns[c].append(slic)

    P(columns)

    vertical_digit_number_lists = []
    P(vertical_digit_number_lists)
    for i in columns:
        op = i.pop().strip()
        vertical_digit_number_list = []
        top_of_column = i[0]
        for jj in range(len(top_of_column)-1,-1,-1):
            vertical_digit = []
            j = top_of_column[jj]
            if j in '0123456789':
                vertical_digit.append(j)
            for kk in range(1,len(i)):
                k = i[kk]
                if k[jj] in '0123456789':
                    vertical_digit.append(k[jj])
            vertical_int = int(''.join(vertical_digit))
            vertical_digit_number_list.append(vertical_int)
        vertical_digit_number_list.append(op)
        
        vertical_digit_number_lists.append(vertical_digit_number_list.copy())

    P(vertical_digit_number_lists)

    c = 0
    for i in vertical_digit_number_lists:
        op = i.pop()
        x = 0
        if op == '+':
            x = sum(i)
        elif op == '*':
            x = math.prod(i)
        P(op,i,x)
        c += x
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
            x = input_file.read()
            input_set = reprocess_input(x)

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