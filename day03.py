import sys
import argparse
from pathlib import Path
import time

def count_trees(filename,slopes):

    with open(filename) as f:
        terrain_grid = f.read()
    height = terrain_grid.count('\n')
    width = terrain_grid.find('\n')
    terrain_grid = terrain_grid.replace('\n', '')

    tree_product = 1
    for s in slopes:
        posx = 0
        posy = 0
        tree_count = 0
        while posy < height:
            if terrain_grid[posy*width+posx] == '#':
                tree_count += 1
            posx = (posx + s[0]) % width
            posy += s[1]
        tree_product *= tree_count

    print(tree_product)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Solution to Advent of Code 2020 Day 03')
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
            count_trees(args.file,[(3,1)])
        else:
            count_trees(args.file,[(1,1),(3,1),(5,1),(7,1),(1,2)])
        end = time.time()
        print( "%f ms" % ((end-start)*1000))