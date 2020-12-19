import sys
import argparse
from pathlib import Path
import itertools
import time

#     0123 4567
# 0   xxxx xxxx
# 1   xxxx xxxx
#     ....
# 127 xxxx xxxx

def get_seat(boarding_code):
    size = [8 >> 1,128 >> 1]
    pos = [0,0]
    for p,c in zip([1] * 7 + [0] * 3, boarding_code):
        if c == 'B' or c == 'R':
            pos[p] += size[p]
        size[p] >>= 1
    return pos[1]*8+pos[0]

def highest_seat_id(filename):
    highest = 0
    with open(filename) as fin:
        for line in fin:
            seat_id = get_seat(line.rstrip())
            if seat_id > highest:
                highest = seat_id
    print(highest)

def find_unoccupied_seat(filename):
    unoccupied = {(t[1]*8+t[0]) : True for t in itertools.product(range(8),range(128))}
    highest = 0
    with open(filename) as fin:
        for line in fin:
            seat_id = get_seat(line.rstrip())
            del unoccupied[seat_id]
    unoccupied = list(unoccupied.keys())
    unoccupied.sort()
    for i in range(1,len(unoccupied)-1):
        if( unoccupied[i-1]+1 != unoccupied[i] and
            unoccupied[i+1]-1 != unoccupied[i]):
            print(unoccupied[i])
            return 

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Solution to Advent of Code 2020 Day 05')
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
            highest_seat_id(args.file)
        else:
            find_unoccupied_seat(args.file)
        end = time.time()
        print( "%f ms" % ((end-start)*1000))