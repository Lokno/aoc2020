import re
import sys
import argparse
from pathlib import Path
import time

line_re = re.compile("([0-9]+)-([0-9]+) ([a-z]): ([a-z]+)")

def count_valid_part1(filename):
    count = 0

    with open(filename) as f:
        for line in f:
            m = line_re.match(line)
            if m:
                min_val = int(m.group(1))
                max_val = int(m.group(2))
                char = m.group(3)
                password = m.group(4)

                if min_val <= password.count(char) <= max_val:
                    count += 1
    print(count)

def count_valid_part2(filename):
    count = 0

    with open(filename) as f:
        for line in f:
            m = line_re.match(line)
            if m:
                val_a = int(m.group(1))
                val_b = int(m.group(2))
                char = m.group(3)
                password = m.group(4)

                if (password[val_a-1] == char) ^ (password[val_b-1] == char):
                    count += 1
    print(count)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Solution to Advent of Code 2020 Day 02')
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
            count_valid_part1(args.file)
        else:
            count_valid_part2(args.file)
        end = time.time()
        print( "%f ms" % ((end-start)*1000))