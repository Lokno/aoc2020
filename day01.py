import sys
import argparse
from pathlib import Path

def find_two_sum(filename,target):
    with open(filename) as f:
        values = {int(v) for v in f.readlines()}

    for a in range(target+1):
        b = target-a
        if a in values and b in values:
            print(a*b)
            return

def find_three_sum(filename,target):
    with open(filename) as f:
        values = {int(v) for v in f.readlines()}

    for a in range(target+1):
        for j in range(target-a+1):
            b = target-a-j
            c = j
            if a in values and b in values and c in values:
                print(a*b*c)
                return


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Solution to Advent of Code 2020 Day 01')
    parser.add_argument('file', help='path to input file')
    parser.add_argument('--part', dest='part', type=int, default=1, choices=range(1, 3), 
                        help='select part (1) or part (2) solution')
    parser.add_argument('--target', dest='target', type=int, default=2020,
                        help='target sum (default 2020)')
    args = parser.parse_args()

    file_path = Path(args.file)

    if args.target < 0:
        print("ERROR: Target must be a positive integer", file=sys.stderr)
    elif not file_path.exists():
        print("ERROR: Input file does not exist", file=sys.stderr)
    elif not file_path.is_file():
        print("ERROR: Input path is not a file", file=sys.stderr)
    else:
        if args.part == 1:
            find_two_sum(args.file,args.target)
        else:
            find_three_sum(args.file,args.target)