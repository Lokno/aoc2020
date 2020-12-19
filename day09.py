import sys
import argparse
from pathlib import Path
import time

def read_values(filename):
    with open(filename) as fin:
        values = [int(v) for v in fin]
    return values

def is_sum(v,head):
    for a in head:
        b = v-a
        if a != b and b in head:
            return True
    return False

def first_invalid_value(values):
    head = values[:25]
    p = 0
    for v in values[25:]:
        if not is_sum(v,head):
            break
        p += 1
        head = values[p:p+25]

    return values[p+25]

def print_invalue_value(filename):
    val = first_invalid_value(read_values(filename))
    print(val)

def find_weakness(filename):
    values = read_values(filename)

    lv = len(values)
    val = first_invalid_value(values)

    for i in range(2,lv-1):
        for j in range(lv-i+1):
            window = values[j:j+i]
            if val == sum(window):
                window.sort()
                print(window[0]+window[-1])
                return


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Solution to Advent of Code 2020 Day 09')
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
            print_invalue_value(args.file)
        else:
            find_weakness(args.file)
        end = time.time()
        print( "%f ms" % ((end-start)*1000))