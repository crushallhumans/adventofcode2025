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
import inspect
from functools import reduce
from functools import cache
from itertools import chain
from multiprocessing import Pool
pp = pprint.PrettyPrinter()

ADVENT_YEAR = '2025'
DEBUG = False
TEST_INPUT_STRING_ONE = """3-5
10-14
16-20
12-18

1
5
8
11
17
32
"""
TEST_INPUT_STRING_TWO = TEST_INPUT_STRING_ONE
TEST_ONE_RESULT = 3
TEST_TWO_RESULT = 14


def reprocess_input(param_set):
    if isinstance(param_set,str):
        l = []
        l = [input_line.strip() for input_line in param_set.splitlines()]
        param_set = {
            'ranges':[],
            'ingredients':[]
        }
        ranges = True
        for i in l:
            if not i:
                ranges = False
                continue
            if ranges:
                ii = i.split('-')
                param_set['ranges'].append((int(ii[0]),int(ii[1]))) # list, not tuple - needs to be modified inline in two_star
            else:
                param_set['ingredients'].append(int(i))
    param_set['ranges'] = sorted(param_set['ranges'])
    return param_set    


def one_star(param_set, is_two_star = False):
    if not is_two_star: print("---------------one_star--------------------")
    param_set = reprocess_input(param_set)
    c = 0
    for i in param_set['ingredients']:
        for j in param_set['ranges']:
            if i >= j[0] and i <= j[1]:
                P(i,'fresh')
                c += 1
                break
    return c

def two_star(param_set):
    print("---------------two_star--------------------")
    #return one_star(param_set,True)
    param_set = reprocess_input(param_set)
    c = 0
    P(param_set['ranges'])

    # karanlyons showed me the way - 
    merged_ranges = [param_set['ranges'][0]]
    for L, R in param_set['ranges']:
        P(L,R)
        P(merged_ranges[-1])
        if merged_ranges[-1][1] >= L:
            P('absorb')
            merged_ranges[-1] = (merged_ranges[-1][0], max(merged_ranges[-1][1], R))
        else:
            P('append')
            merged_ranges.append((L,R))
    P(merged_ranges)
    for i in merged_ranges:
        c += i[1] - (i[0]-1)
    return c



    final_sets = { param_set['ranges'].pop(0) }
    # for check_set in param_set['ranges']:
    #     P()
    #     P('check')
    #     P(check_set)
    #     P(final_sets)
    final_sets, _ = eval_sets(param_set['ranges'], final_sets)

    P(sorted(final_sets))

    for i in final_sets:
        c += i[1] - (i[0]-1)

    return c


# I was close, but got lost around the sorting and recursion rechecking!
#result attempts:
#361200577741617 too high
#334xxxxxxxxx710 correct
#333876515575290 too low
def eval_sets(check_sets, final_sets, fully_removed = set(), recur = 1):
    P('--check_sets--')
    P(sorted(check_sets))
    for check_set in sorted(check_sets):
        is_disjoint = set()
        is_not_disjoint = set()
        no_extensions = True
        P('--check_set--')
        P(check_set)
        P('--test_sets--')
        P(sorted(final_sets))
        P('---------------')
        for test_set in sorted(final_sets):
            P('--test_set--')
            P(test_set)
            changes = {
                'remove':[],
                'add':[]
            }
            if check_set == test_set:
                P('skipping')
                continue
            answer = extends(check_set, test_set)
            P('!!',answer)
            if 'disjoint' in answer and answer['disjoint']:
                if check_set not in is_disjoint and check_set not in final_sets:
                    P('reported disjoint: ',answer['disjoint'])
                    is_disjoint.add(check_set)
            else:
                P('exclude disjoint: ',check_set)
                is_not_disjoint.add(check_set)
                if 'left' in answer and answer['left']:
                    no_extensions = False
                    changes['remove'].append(test_set)
                    changes['add'].append((check_set[0],test_set[1]))
                elif 'right' in answer and answer['right']:
                    no_extensions = False
                    changes['remove'].append(test_set)
                    changes['add'].append((test_set[0],check_set[1]))
                elif 'full_overlap' in answer and answer['full_overlap']:
                    changes['remove'].append(test_set)
                    changes['add'].append(check_set)
            P('!!!!!!!!!!!!!!!!!')
            P('no_extensions',no_extensions)
            P('??',changes)
            
        for i in changes['remove']:
            if i in final_sets:
                fully_removed.add(i)
                final_sets.remove(i)
        for i in is_disjoint:
            if i not in is_not_disjoint:
                P('actual disjoint: ',i)
                if i not in fully_removed:
                    changes['add'].append(i)
        for i in changes['add']:
            if i not in fully_removed:
                final_sets.add(i)

        # # recurse to recheck all if we've extended any of them
        # while not no_extensions:        
        #     P('extension - delving')
        if recur < 4:
            final_sets, no_extensions = eval_sets(final_sets.copy(), final_sets.copy(),fully_removed=fully_removed, recur = recur + 1)

        P('final set - ',sorted(final_sets))

    P('*******************************')
    P()
    return final_sets, no_extensions

def extends(c,t): #check_set, #test_set
    extensions = {
        'left' : False,
        'right': False,
        'full_overlap' : False,
        'disjoint' : False,
    }
    P(c,t)
    if (
            (c[0] <  t[0]) # check set left side is left of test set left side
        and (c[1] >= t[0]) # check set right side is right of test set left side, or connected
    ):
        extensions['left'] = True
    
    if (
            (c[1] >  t[1]) # check set right side is right of test set right side
        and (c[0] <= t[1]) # check set left side is left of test set right side, or connected
    ):
        extensions['right'] = True
    
    if extensions['left'] and extensions['right']:
        extensions = {'full_overlap': True}
    elif not extensions['left'] and not extensions['right']:
        extensions = {'disjoint': c}

    return extensions




#---------------------------------------------------------
def P(*args, force = False, end = "\n"):
    if DEBUG or force:
        # current_frame = inspect.currentframe()
        # # Get the caller's frame (one level up)
        # caller_frame = current_frame.f_back
        # # Get the line number from the caller's frame
        # line_number = str(caller_frame.f_lineno)    
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
        P(e,type(e),force=True)