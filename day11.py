import sys
import argparse
from pathlib import Path

def read_grid(filename):
    xdim = 0
    ydim = 0
    with open(filename) as fin:
        grid = fin.read()
        xdim = grid.find('\n')
        ydim = grid.count('\n')
        grid = list(grid.replace('\n',''))
    return (grid,xdim,ydim)

def count_adjacent(x,y,xdim,ydim,t,g):
    s = 0
    offsets = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
    for ox,oy in offsets:
        px = x+ox
        py = y+oy
        if px >= 0 and py >= 0 and px < xdim and py < ydim and g[py*xdim+px] == t:
            s += 1
    return s

def count_adjacent_occupied_ray(x,y,xdim,ydim,g):
    s = 0
    offsets = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
    for ox,oy in offsets:
        px = x+ox
        py = y+oy
        while px >= 0 and py >= 0 and px < xdim and py < ydim:
            seat = g[py*xdim+px]
            if seat == 'L':
                break
            if seat == '#':
                s += 1
                break
            px += ox
            py += oy
    return s

def grid_sim_part1(filename):
    grid,xdim,ydim = read_grid(filename)

    pgrid = list(grid)

    first = True

    while first or pgrid != grid:
        first = False
        # swap
        tmp = grid
        grid = pgrid
        pgrid = tmp
        for x in range(xdim):
            for y in range(ydim):
                s = grid[y*xdim+x]
                aocc = count_adjacent(x,y,xdim,ydim,'#',grid)
                if s == 'L' and aocc == 0:
                    s = '#'
                elif s == '#' and aocc >= 4:
                    s = 'L'
                pgrid[y*xdim+x] = s

    print(grid.count('#'))

def grid_sim_part2(filename):
    grid,xdim,ydim = read_grid(filename)

    pgrid = list(grid)

    first = True

    while first or pgrid != grid:
        first = False
        # swap
        tmp = grid
        grid = pgrid
        pgrid = tmp
        for x in range(xdim):
            for y in range(ydim):
                s = grid[y*xdim+x]
                aocc = count_adjacent_occupied_ray(x,y,xdim,ydim,grid)
                if s == 'L' and aocc == 0:
                    s = '#'
                elif s == '#' and aocc >= 5:
                    s = 'L'
                pgrid[y*xdim+x] = s

    print(grid.count('#'))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Solution to Advent of Code 2020 Day 11')
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
            grid_sim_part1(args.file)
        else:
            grid_sim_part2(args.file)