import sys
import argparse
from pathlib import Path
from itertools import chain,product
from collections import deque
import copy
import time

def read_grid(filename):
    data = {}

    with open(filename) as f:
        grid = f.read()

    data['height'] = grid.count('\n')
    data['width'] = grid.find('\n')
    data['grid'] = grid.replace('\n', '')

    return data


def cidx4(x,y,z,w,dx,dy,dz):
    return w*dx*dy*dz+z*dx*dy+y*dx+x

def is_active4(grid, x, y, z, w, dims):
    dx,dy,dz,dw = dims
    return True if (0 <= x < dx and 0 <= y < dy and 0 <= z < dz and 0 <= w < dw and grid[w][z][y][x] == '#') else False

def set_type4(grid, x, y, z, w, dims, c):
    dx,dy,dz,dw = dims
    if 0 <= x < dx and 0 <= y < dy and 0 <= z < dz and 0 <= w < dw:
        grid[w][z][y][x] = c

def count_neighbors4( grid, x, y, z, w, dims ):
    neighbors = ((-1,-1,-1,-1),(-1,-1,-1, 0),(-1,-1,-1, 1),(-1,-1, 0,-1),(-1,-1, 0, 0),
                 (-1,-1, 0, 1),(-1,-1, 1,-1),(-1,-1, 1, 0),(-1,-1, 1, 1),(-1, 0,-1,-1),
                 (-1, 0,-1, 0),(-1, 0,-1, 1),(-1, 0, 0,-1),(-1, 0, 0, 0),(-1, 0, 0, 1),
                 (-1, 0, 1,-1),(-1, 0, 1, 0),(-1, 0, 1, 1),(-1, 1,-1,-1),(-1, 1,-1, 0),
                 (-1, 1,-1, 1),(-1, 1, 0,-1),(-1, 1, 0, 0),(-1, 1, 0, 1),(-1, 1, 1,-1), 
                 (-1, 1, 1, 0),(-1, 1, 1, 1),( 0,-1,-1,-1),( 0,-1,-1, 0),( 0,-1,-1, 1), 
                 ( 0,-1, 0,-1),( 0,-1, 0, 0),( 0,-1, 0, 1),( 0,-1, 1,-1),( 0,-1, 1, 0), 
                 ( 0,-1, 1, 1),( 0, 0,-1,-1),( 0, 0,-1, 0),( 0, 0,-1, 1),( 0, 0, 0,-1),
                 ( 0, 0, 0, 1),( 0, 0, 1,-1),( 0, 0, 1, 0),( 0, 0, 1, 1),( 0, 1,-1,-1), 
                 ( 0, 1,-1, 0),( 0, 1,-1, 1),( 0, 1, 0,-1),( 0, 1, 0, 0),( 0, 1, 0, 1), 
                 ( 0, 1, 1,-1),( 0, 1, 1, 0),( 0, 1, 1, 1),( 1,-1,-1,-1),( 1,-1,-1, 0), 
                 ( 1,-1,-1, 1),( 1,-1, 0,-1),( 1,-1, 0, 0),( 1,-1, 0, 1),( 1,-1, 1,-1), 
                 ( 1,-1, 1, 0),( 1,-1, 1, 1),( 1, 0,-1,-1),( 1, 0,-1, 0),( 1, 0,-1, 1), 
                 ( 1, 0, 0,-1),( 1, 0, 0, 0),( 1, 0, 0, 1),( 1, 0, 1,-1),( 1, 0, 1, 0), 
                 ( 1, 0, 1, 1),( 1, 1,-1,-1),( 1, 1,-1, 0),( 1, 1,-1, 1),( 1, 1, 0,-1), 
                 ( 1, 1, 0, 0),( 1, 1, 0, 1),( 1, 1, 1,-1),( 1, 1, 1, 0),( 1, 1, 1, 1))
    return sum([1 for ox,oy,oz,ow in neighbors if is_active4(grid,x+ox,y+oy,z+oz,w+ow,dims)])

def expand4(grid, dims):
    dimx,dimy,dimz,dimw = dims

    emptz = deque()
    for y in range(dimy+2):
        xque = deque(['.']*(dimx+2))
        emptz.append(xque)

    for zque in grid:
        for yque in zque:
            for xque in yque:
                xque.appendleft('.')
                xque.append('.')
            yque.appendleft(deque(['.']*(dimx+2)))
            yque.append(deque(['.']*(dimx+2)))

        zque.appendleft(copy.deepcopy(emptz))
        zque.append(copy.deepcopy(emptz))

    topz = deque()
    botz = deque()
    for z in range(dimz+2):
        topz.appendleft(copy.deepcopy(emptz))
        botz.append(copy.deepcopy(emptz))

    grid.appendleft(topz)
    grid.append(botz)

def count_active4(grid,dims):
    dimx,dimy,dimz,dimw = dims
    count = 0
    for y,z,w in product(range(dimy),range(dimz),range(dimw)):
        count += grid[w][z][y].count('#')
    return count



def cidx3(x,y,z,dx,dy):
    return z*dx*dy+y*dx+x

def is_active3(grid, x, y, z, dims):
    dx,dy,dz = dims
    return True if (0 <= x < dx and 0 <= y < dy and 0 <= z < dz and grid[z][y][x] == '#') else False

def set_type3(grid, x, y, z, dims, c):
    dx,dy,dz = dims
    if 0 <= x < dx and 0 <= y < dy and 0 <= z < dz:
        grid[z][y][x] = c

def count_neighbors3( grid, x, y, z, dims ):
    neighbors = ((-1,-1,-1),(-1,-1, 0),(-1,-1, 1),(-1, 0,-1),(-1, 0, 0),
                 (-1, 0, 1),(-1, 1,-1),(-1, 1, 0),(-1, 1, 1),( 0,-1,-1),
                 ( 0,-1, 0),( 0,-1, 1),( 0, 0,-1),( 0, 0, 1),( 0, 1,-1),
                 ( 0, 1, 0),( 0, 1, 1),( 1,-1,-1),( 1,-1, 0),( 1,-1, 1),
                 ( 1, 0,-1),( 1, 0, 0),( 1, 0, 1),( 1, 1,-1), (1, 1, 0), (1, 1, 1))
    return sum([1 for ox,oy,oz in neighbors if is_active3(grid,x+ox,y+oy,z+oz,dims)])

def expand3(grid, dims):
    dimx,dimy,dimz = dims

    for yque in grid:
        for xque in yque:
            xque.appendleft('.')
            xque.append('.')
        yque.appendleft(deque(['.']*(dimx+2)))
        yque.append(deque(['.']*(dimx+2)))

    empty = deque()
    for y in range(dimy+2):
        xque = deque(['.']*(dimx+2))
        empty.append(xque)

    grid.appendleft(empty)
    grid.append(copy.deepcopy(empty))

def count_active3(grid,dims):
    dimx,dimy,dimz = dims
    count = 0
    for y,z in product(range(dimy),range(dimz)):
        count += grid[z][y].count('#')
    return count

def print_grid3(grid,dims):
    dimx,dimy,dimz = dims
    for z in range(dimz):
        print("z=%d" % (z-int(dimz/2)))
        for y in range(dimy):
            s = ''
            for x in range(dimx):
                s += '#' if is_active3(grid,x,y,z,dims) else '.'
            print(s)

def wrap(l,n):
    return deque([deque(l[i:i + n]) for i in range(0, len(l), n)])

def conway3d(filename,cycles):
    grid_data = read_grid(filename)

    dims = (grid_data['width'],grid_data['height'],1)

    grid = deque()
    grid.append(wrap(list(grid_data['grid']),grid_data['width']))
    gridb = copy.deepcopy(grid)
    
    cycle = 0
    while cycle < cycles:
        cycle += 1
        dimx,dimy,dimz = dims
        expand3(grid,dims)
        expand3(gridb,dims)
        dims = (dimx+2,dimy+2,dimz+2)
        dimx,dimy,dimz = dims
        for x,y,z in product(range(dimx),range(dimy),range(dimz)):
            nc = count_neighbors3(grid,x,y,z,dims)
            oc = '.'
            if is_active3(grid,x,y,z,dims):
                if nc == 2 or nc == 3:
                    oc = '#'
            elif nc == 3:
                oc = '#'

            set_type3(gridb,x,y,z,dims,oc)

        #swap grid
        tmp = gridb
        gridb = grid
        grid = tmp

    print(count_active3(grid,dims))

def conway4d(filename,cycles):
    grid_data = read_grid(filename)

    dims = (grid_data['width'],grid_data['height'],1,1)

    grid = deque()
    grid.append(deque())
    grid[0].append(wrap(list(grid_data['grid']),grid_data['width']))
    gridb = copy.deepcopy(grid)
    
    cycle = 0
    while cycle < cycles:
        cycle += 1
        dimx,dimy,dimz,dimw = dims
        expand4(grid,dims)
        expand4(gridb,dims)
        dims = (dimx+2,dimy+2,dimz+2,dimw+2)
        dimx,dimy,dimz,dimw = dims
        for x,y,z,w in product(range(dimx),range(dimy),range(dimz),range(dimw)):
            nc = count_neighbors4(grid,x,y,z,w,dims)
            oc = '.'
            if is_active4(grid,x,y,z,w,dims):
                if nc == 2 or nc == 3:
                    oc = '#'
            elif nc == 3:
                oc = '#'

            set_type4(gridb,x,y,z,w,dims,oc)

        #swap grid
        tmp = gridb
        gridb = grid
        grid = tmp

    print(count_active4(grid,dims))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Solution to Advent of Code 2020 Day 17')
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
            conway3d(args.file,6)
        else:
            conway4d(args.file,6)
        end = time.time()
        print( "%f ms" % ((end-start)*1000))