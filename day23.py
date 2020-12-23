import sys
import argparse
from pathlib import Path
import time,signal
from collections import deque

import numpy as np

def read_sequence(filename):
    with open(filename) as f:
        return deque([int(x) for x in list(f.read())])

def read_sequence_np(filename):
    with open(filename) as f:
        return np.array([int(x) for x in list(f.read())])

# current is the end of the deque seq[-1]
def move(seq):

    minv = min(seq)
    maxv = max(seq)

    seq.rotate(-1)

    pickup = deque([seq.popleft() for i in range(3)])

    dst = ((seq[-1] - 2) % maxv)+1

    while dst in pickup:
        dst = ((dst - 2) % maxv)+1

    didx = seq.index(dst)
    for i in range(3):
        seq.insert((didx+1) % (maxv+1), pickup.pop())

def move_np(seq):

    minv = min(seq)
    maxv = max(seq)

    seq = np.roll(seq,-4)

    pickup = seq[-3:]
    seq = seq[:-3]

    dst = ((seq[-1] - 2) % maxv)+1

    while dst in pickup:
        dst = ((dst - 2) % maxv)+1

    didx = np.where(seq == dst)[0][0]

    seq = np.concatenate( (seq[:didx+1],pickup,seq[didx+1:]), axis=None )

    return seq

def part1_np(filename,n):
    seq = read_sequence_np(filename)

    for i in range(n):
        seq = move_np(seq)

    one_idx = np.where(seq == 1)[0][0]
    seq = np.roll(seq,-one_idx-1)

    print(''.join([str(x) for x in seq[:-1]]))

def part2_np(filename,n):
    seq = read_sequence(filename)

    minv = min(seq)
    maxv = max(seq)

    seq = np.concatenate( (seq, np.arange(maxv,1000000)), axis=None )

    maxv = max(seq)

    for i in range(n):
        seq = np.roll(seq,-4)
        pickup = seq[-3:]
        seq = seq[:-3]
        dst = ((seq[-1] - 2) % maxv)+1

        while dst in pickup:
            dst = ((dst - 2) % maxv)+1

        didx = np.where(seq == dst)[0][0]
        seq = np.concatenate( (seq[:didx+1],pickup,seq[didx+1:]), axis=None )

    idx = np.where(seq == 1)[0][0]

    numa = seq[(idx+1) % 1000000]
    numb = seq[(idx+2) % 1000000]

    print(numa*numb)

def part1(filename,n):
    seq = read_sequence(filename)

    for i in range(n):
        move(seq)

    seq.rotate(-seq.index(1)-1)

    print(''.join([str(x) for x in seq][:-1]))

def part2(filename,n):
    seq = read_sequence(filename)

    maxv = max(seq)
    i = len(seq)

    while i < 1000000:
        seq.append(i)
        i += 1

    for i in range(n):
        move(seq)

    idx = seq.index(1)

    numa = seq[(idx+1) % 1000000]
    numb = seq[(idx+2) % 1000000]

    print(numa*numb)

# end_program = False

# def signal_handler(sig, frame):
#     global end_program
#     print('Aborting...')
#     end_program = True

# signal.signal(signal.SIGINT, signal_handler)

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
        start = time.time()
        if args.part == 1:
            part1_np(args.file,100)
        else:
            part2_np(args.file,10000000)
        end = time.time()
        print( "%f ms" % ((end-start)*1000))