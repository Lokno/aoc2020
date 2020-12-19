import sys
import argparse
from pathlib import Path
import time

def run_code(code):

    ops = {
        'acc' : lambda val: (val,1),
        'jmp' : lambda val: (0,val),
        'nop' : lambda val: (0,1),
    }

    visited = set()
    instuction_run_twice = False
    accumulator = 0
    pos = 0
    while pos < len(code):
        op,val = code[pos]
        if pos not in visited:
            visited.add(pos) 
            amt,step = ops[op](int(val))
            accumulator += amt
            pos += step
        else:
            instuction_run_twice = True
            break

    return (accumulator,instuction_run_twice)

def identify_infinite_loop_and_exit(filename):

    with open(filename) as fin:
        code = [x.rstrip().split(' ') for x in fin.readlines()]

    accumulator,instuction_run_twice = run_code(code)

    print(accumulator)


def correct_infinite_loop(filename):

    with open(filename) as fin:
        code = [x.rstrip().split(' ') for x in fin.readlines()]

    nops = [i for i,op in enumerate(code) if op[0] == 'nop']
    jmps = [i for i,op in enumerate(code) if op[0] == 'jmp']

    for idx in nops:
        code[idx][0] = 'jmp'
        accumulator,instuction_run_twice = run_code(code)
        if not instuction_run_twice:
            print(accumulator)
            break
        code[idx][0] = 'nop'

    for idx in jmps:
        code[idx][0] = 'nop'
        accumulator,instuction_run_twice = run_code(code)
        if not instuction_run_twice:
            print(accumulator)
            break
        code[idx][0] = 'jmp'


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Solution to Advent of Code 2020 Day 08')
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
            identify_infinite_loop_and_exit(args.file)
        else:
            correct_infinite_loop(args.file)
        end = time.time()
        print( "%f ms" % ((end-start)*1000))