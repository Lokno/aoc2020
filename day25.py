import sys
import argparse
from pathlib import Path
import time
import signal
import itertools

def read_lines(filename):
    with open(filename) as fin:
        data = [int(line) for line in fin ]
    return data

def part1(filename):
    transform = lambda x,s: (x*s) % 20201227

    publica,publicb = read_lines(filename)

    val = 1
    ekey = 1
    while val != publica:
        val = transform(val,7)
        ekey = transform(ekey,publicb)

    print(ekey)

def part2(filename):
    print("There is no part 2")

end_program = False

def signal_handler(sig, frame):
    global end_program
    print('Aborting...')
    end_program = True

signal.signal(signal.SIGINT, signal_handler)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Solution to Advent of Code 2020 Day 25')
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
            part1(args.file)
        else:
            part2(args.file)
        end = time.time()
        print( "%f ms" % ((end-start)*1000))