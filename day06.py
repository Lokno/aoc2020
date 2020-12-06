import sys
import argparse
from pathlib import Path

def count_anyone(filename):
    with open(filename) as fin:
        data_str = fin.read()

    entries = data_str.split('\n\n')

    sum_unique = 0
    for e in entries:
        sum_unique += len(set(e.replace('\n','')))

    print(sum_unique)

def count_everyone(filename):
    with open(filename) as fin:
        data_str = fin.read()

    entries = data_str.split('\n\n')

    sum_unique = 0
    for e in entries:
        party = [set(s) for s in e.rstrip().split('\n')]
        party_intersection = party[0]
        for member in party[1:]:
            party_intersection = party_intersection.intersection(member)
        sum_unique += len(party_intersection)

    print(sum_unique)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Solution to Advent of Code 2020 Day 06')
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
            count_anyone(args.file)
        else:
            count_everyone(args.file)