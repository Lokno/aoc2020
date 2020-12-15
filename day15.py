import sys
import argparse
from pathlib import Path

def read_sequence(filename):
    with open(filename) as fin:
        data = [int(x) for x in fin.readline().split(',')]
    return data

def nth_spoken(filename,n):
    sn = read_sequence(filename)

    lh = {}

    turn = 1
    last = -1

    for num in sn:
        lh[num] = turn
        last = num
        turn += 1

    while turn <= n:
        hval = lh.get(last)
        lh[last] = turn-1
        last = 0 if hval is None else turn-1-hval
        turn += 1

    print(last)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Solution to Advent of Code 2020 Day XX')
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
            nth_spoken(args.file,2020)
        else:
            nth_spoken(args.file,30000000)