import sys
import argparse
from pathlib import Path
import math
from operator import mul
from functools import reduce

def read_data(filename):
    data = {}
    with open(filename) as fin:
        data['timestamp'] = fin.readline().rstrip()
        data['ids'] = fin.readline().rstrip().split(',')
    return data

def next_multiple(num,factor):
    return int(math.ceil(num / factor))*factor

def is_multiple(num,factor):
    return num % factor == 0

def part1(filename):
    data = read_data(filename)

    earliest_time = 2**32-1
    earliest_bus = -1
    ntimestamp = int(data['timestamp'])

    for id in data['ids']:
        if id == 'x':
            continue

        nid = int(id)
        t = int(math.ceil(ntimestamp / nid))*nid

        if t < earliest_time:
            earliest_time = t
            earliest_bus = nid

    print(earliest_bus*(earliest_time-ntimestamp))

def part2(filename):
    data = read_data(filename)

    ids = [(offset,int(id)) for offset,id in enumerate(data['ids']) if id != 'x']

    t = 0
    n = 1
    lined_up_count = 0

    found = False
    while not found:
        found = True
        lined_up = []

        next_arrival = next_multiple(t,ids[0][1])

        for offset,id in ids:
            if not is_multiple(next_arrival+offset, id):
                found = False
            else:
                lined_up.append(id)

        if found:
            print(t)
            return

        if lined_up_count < len(lined_up):
            lined_up_count = len(lined_up)
            n = reduce(mul,lined_up)

        t += n

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Solution to Advent of Code 2020 Day 13')
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
        if args.part == 1:
            part1(args.file)
        else:
            part2(args.file)