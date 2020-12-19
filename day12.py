import sys
import argparse
from pathlib import Path
import time

def read_data(filename):
    with open(filename) as fin:
        data = [{'char' : v[:1], 'val' : int(v[1:])} for v in fin]
    return data

def calculate_distance(filename):
    data = read_data(filename)

    heading = 'E'
    pos = [0,0]

    c2i  = {'N': 0, 'E': 1, 'S': 2, 'W': 3}
    i2c  = {0: 'N', 1: 'E', 2: 'S', 3: 'W'}
    dirs = ((0, 1), (1, 0), (0, -1), (-1, 0))

    for action in data:
        op = action['char']
        amt = action['val']
        if op == 'F':
            op = heading
        if op == 'L':
            heading = i2c[(c2i[heading] - int(amt / 90)) % 4]
        elif op == 'R':
            heading = i2c[(c2i[heading] + int(amt / 90)) % 4]
        else:
            d = dirs[c2i[op]]
            pos[0] += d[0] * amt
            pos[1] += d[1] * amt

    print(abs(pos[0]) + abs(pos[1]))

def calculate_distance_with_waypoint(filename):
    data = read_data(filename)

    ship_pos = [0,0]
    wayp_pos = [10,1] # relative

    dirs = {'N':(0, 1), 'E':(1, 0), 'S':(0, -1), 'W':(-1, 0)}

    rot = {'L' : lambda p: [-p[1],p[0]],
           'R' : lambda p: [p[1],-p[0]]}

    for action in data:
        op = action['char']
        amt = action['val']
        if op == 'F':
            ship_pos[0] += wayp_pos[0] * amt
            ship_pos[1] += wayp_pos[1] * amt
        elif op == 'L' or op == 'R':
            for i in range(int(amt / 90)):
                wayp_pos = rot[op](wayp_pos)
        else:
            d = dirs[op]
            wayp_pos[0] += d[0] * amt
            wayp_pos[1] += d[1] * amt

    print(abs(ship_pos[0]) + abs(ship_pos[1]))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Solution to Advent of Code 2020 Day 12')
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
            calculate_distance(args.file)
        else:
            calculate_distance_with_waypoint(args.file)
        end = time.time()
        print( "%f ms" % ((end-start)*1000))