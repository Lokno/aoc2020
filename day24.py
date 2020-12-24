import sys
import argparse
from pathlib import Path
import time
import signal
import re
import math
from copy import deepcopy
from itertools import product

hex_re = re.compile('(ne|nw|se|sw|e|w)')

def ne(a,b):
    ep = 0.00000
    ax,ay = a
    bx,by = b
    dx = abs(ax-bx)
    dy = abs(ay-by)
    return dx < ep and dy < ep

def read_paths(filename):
    with open(filename) as fin:
        paths = [hex_re.findall(line) for line in fin]
    return paths

def update_bounds( x, y, minc, maxc ):
    minx,miny = minc
    maxx,maxy = maxc

    if x < minx:
        minc[0] = x
    elif x > maxx:
        maxc[0] = x
    if y < miny:
        minc[1] = y
    elif y > maxy:
        maxc[1] = y

# Odd rows are right shifted
odd  = {'se':( 0,-1), 'ne':( 0, 1), 'sw':( 1,-1), 'nw':( 1, 1), 'w':( 1, 0), 'e':(-1, 0) }
even = {'se':(-1,-1), 'ne':(-1, 1), 'sw':( 0,-1), 'nw':( 0, 1), 'w':( 1, 0), 'e':(-1, 0) }

def calc_flipped_from_paths(filename):
    paths = read_paths(filename)

    tiles = {}  # all tiles start out white (false) 

    minc = [0,0]
    maxc = [0,0]

    for p in paths:
        x,y = (0,0)
        for d in p:
            ox,oy = even[d] if (y%2 == 0) else odd[d]
            x,y = (x+ox,y+oy)
        np = x,y
        if np in tiles:
            tiles[np] = not tiles[np]
        else:
            tiles[np] = True
            update_bounds(x,y,minc,maxc)

    return tiles,minc,maxc

def update_tiles(tiles,minc,maxc):
    tilesb = deepcopy(tiles)

    for x,y in product(range(minc[0]-2,maxc[0]+2),range(minc[1]-2,maxc[1]+2)):
        isblk = tiles.get((x,y))
        isblk = False if isblk is None else isblk  # all tiles start out white (false)

        count = 0
        offsets = even if (y%2 == 0) else odd
        
        for ox,oy in offsets.values():
            adj_is_blk = tiles.get((x+ox,y+oy))
            if adj_is_blk is not None and adj_is_blk == True:
                count += 1

        if (isblk and (count == 0 or count > 2)) or (not isblk and count == 2):
            if (x,y) in tiles:
                tilesb[(x,y)] = not tiles[(x,y)]
            else:
                tilesb[(x,y)] = True
                update_bounds(x,y,minc,maxc)

    return tilesb

def part1(filename):
    tiles,minc,maxc = calc_flipped_from_paths(filename)
    print(list(tiles.values()).count(True))

def part2(filename,days):
    tiles,minc,maxc = calc_flipped_from_paths(filename)

    for i in range(days):
        tiles = update_tiles(tiles,minc,maxc)
        
    print(list(tiles.values()).count(True))

end_program = False

def signal_handler(sig, frame):
    global end_program
    print('Aborting...')
    end_program = True

signal.signal(signal.SIGINT, signal_handler)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Solution to Advent of Code 2020 Day 24')
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
            part2(args.file,100)
        end = time.time()
        print( "%f ms" % ((end-start)*1000))