import sys
import argparse
from pathlib import Path
from itertools import product
import time

def read_data(filename):
    data = {}

    with open(filename) as fin:
        data_str = fin.read()

    entries = data_str.split('\n\n')

    data['rules'] = {}
    for line in entries[0].split('\n'):
        num,rest = line.split(':')
        ld = {}
        if rest == ' "a"' or rest == ' "b"':
            ld['type'] = 'S'
            ld['char'] = rest[2]
        else:
            ld['options'] = tuple([tuple([int(n) for n in sect.strip().split(' ')]) for sect in rest.split('|')])
            ld['type'] = 'C'

        data['rules'][int(num)] = ld

    data['msgs'] = entries[1].rstrip().split('\n')

    return data

def match_rule_from( msg, pos, rkey ):
    global data

    lm = len(msg)

    if pos >= lm:
        return (False,0)
    
    rule = data['rules'][rkey]

    if rule['type'] == 'S':
        return (True,1) if msg[pos] == rule['char'] else (False,1)

    truth = False
    l = 0
    for subrules in rule['options']:
        srules_true = True
        l = 0
        for i,subrule in enumerate(subrules):

            srule_match,sl = match_rule_from(msg, pos+l, subrule)
            
            if not srule_match:
                srules_true = False
                break
            l += sl

        if srules_true:
            truth = True
            break

    return (truth,l)

#  0:  8 | 11
#  8: 42 | 42 8
# 11: 42 31 | 42 11 31
def match_cyclic_rule_0( msg, pos):
    global data
    lm = len(msg)

    sslen = lm-pos

    truth = False
    i = 0
    rule_matchA = True
    countA = 0
    while rule_matchA:
        rule_matchA,match_len = match_rule_from( msg, pos+i, 42 )

        if rule_matchA:
            countA += 1
            i += match_len
            j = i
            rule_matchB = True
            countB = 0
            while rule_matchB:
                rule_matchB,match_len = match_rule_from( msg, pos+j, 31 )
                if rule_matchB:
                    countB += 1
                    j += match_len

            if pos+j == sslen and countA > countB and countB > 0:
                truth = True
                break

    return (truth,sslen)

def solve_noncyclic_rule(filename, ridx):
    global data
    data = read_data(filename)

    count = 0
    for msg in data['msgs']:
        t,l = match_rule_from(msg,ridx,0)
        if t and l == len(msg):
            count += 1

    print(count)

def solve_cyclic_rule_0(filename):
    global data
    data = read_data(filename)

    data['rules'][8] = {'type' : 'C', 'options' : ((42,),(42,8))}
    data['rules'][11] = {'type' : 'C', 'options' : ((42,31),(42,11,31))}

    count = 0
    for msg in data['msgs']:
        t,l = match_cyclic_rule_0(msg,0)
        if t and l == len(msg):
            count += 1 
    print(count)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Solution to Advent of Code 2020 Day 19')
    parser.add_argument('file', help='path to input file')
    parser.add_argument('--part', dest='part', type=int, default=1, choices=range(1, 3), 
                        help='select part (1) or part (2) solution')
    args = parser.parse_args()

    file_path = Path(args.file)

    if not file_path.exists():
        print("ERROR: Input file does not exist", file=sys.stderr)
    elif not file_path.is_file():
        print("ERROR: Input path is not a file", file=sys.stderr)
    else:
        start = time.time()
        if args.part == 1:
            solve_noncyclic_rule(args.file, 0)
        else:
            solve_cyclic_rule_0(args.file)
        end = time.time()
        print( "%f ms" % ((end-start)*1000))
