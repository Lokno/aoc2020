import sys
import argparse
from pathlib import Path
import time
from itertools import product,permutations
import sys
import copy
import math
from queue import Queue
import random
import signal

from textwrap import wrap

cwt = {'n':0,'w':1,'s':2,'e':3}
twc = {3:'e', 2:'s', 1:'w', 0:'n'}
off = {'n':(0, 1),'w':(1, 0),'s':(0, -1),'e':(-1, 0)}
opp = {'n':'s','w':'e','s':'n','e':'w'}

def read_grid(file_str):
    data = {}

    data['height'] = file_str.count('\n')+1
    data['width'] = file_str.find('\n')
    data['grid'] = list(file_str.replace('\n', ''))

    return data

def read_grids(filename):
    data = {'tiles':{}}
    with open(filename) as fin:
        data_str = fin.read()

    entries = data_str.rstrip().split('\n\n')

    tile_count = 0

    for entry in entries:
        header, grid = entry.split('\n', 1)
        tile_num = int(header.split(' ')[1][:-1])
        gd = {'tile_num' : tile_num}

        gd.update(read_grid(grid))

        if gd['width'] != gd['height']:
            print('ERROR: Tiles Dimensions Must Be Square')
            sys.exit(-1)

        data['tiles'][tile_num] = gd
        tile_count += 1

    atile = next(iter(data['tiles'].values()))

    data['size'] = atile['width']
    data['total_tiles'] = tile_count
    data['super_size'] = int(math.sqrt(data['total_tiles']))

    return data

# Not Used
def flip_grid( grid, w, h, we, ns ):
    if we:
        for x,y in product(range(int(w/2)),range(h)):
            ia = y*w+x
            ib = y*w+w-1-x
            tmp = grid[ia]
            grid[ia] = grid[ib]
            grid[ib] = tmp

    if ns:
        for x,y in product(range(w),range(int(h/2))):
            ia = (h-1-y)*w+x
            ib = (h-1-y)*w+x
            tmp = grid[ia]
            grid[ia] = grid[ib]
            grid[ib] = tmp

    return grid

# Not Used
def rotate_grid( grid, w, h, cw_rot ):
    ngrid = [''] * w*h
    for x,y in product(range(w),range(h)):
        nx,ny = x,y
        for i in range(cw_rot):
            nx,ny = ny,-nx
        ngrid[ny*w+nx] = grid[y*w+x]

    return ngrid

def trans_copy(grid, w, h, cwr, fwe, fns):
    grid = flip_grid( list(grid), w, h, fwe, fns )
    grid = rotate_grid( grid, w, h, cwr )
    return grid

#        N
#     0 1 .. n
#   n +------+ 0
#   . |      | 1
# E . |      | . W
#   1 |      | .
#   0 +------- n
#     n .. 1 0
#        E

def get_edge_vec( gd ):
    w,h = gd['width'],gd['height']

    edge_temp = {'tile_num': gd['tile_num'], 'dir' : '', 'edge' : '' }

    nort = gd['grid'][:w]
    sout = gd['grid'][(h-1)*w:][::-1]
    east = []
    west = []

    for i in range(h):
        east.append(gd['grid'][(h-1-i)*w])
        west.append(gd['grid'][i*w+w-1])

    dict(edge_temp)

    nd = dict(edge_temp)
    sd = dict(edge_temp)
    ed = dict(edge_temp)
    wd = dict(edge_temp)

    nd['dir'] = 'n'
    sd['dir'] = 's'
    ed['dir'] = 'e'
    wd['dir'] = 'w'

    nd['edge'] = ''.join(nort) 
    sd['edge'] = ''.join(sout)
    ed['edge'] = ''.join(east)
    wd['edge'] = ''.join(west)

    return nd,sd,ed,wd

def print_sgrid( simg ):

    minx,miny = simg['min']
    maxx,maxy = simg['max']

    sstr = ''

    for y in range(miny,maxy+1):
        for x in range(minx,maxx+1):
            if (x,y) in simg:
                print("Corner: %s %s %s" % (simg[(x,y)]['tile_num'],str((x,y)), str((simg[(x,y)]['transform']))))
                sstr += '+'
            else:
                sstr += ' '

        sstr += '\n'

    print(sstr)

def print_image( data, simg, ss ):

    minx,miny = simg['min']
    maxx,maxy = simg['max']

    s = data['size'] 

    sxn = (maxx-minx+1)
    syn = (maxy-miny+1)

    sg = [' '] * sxn * syn * (s+1) * (s+1)

    print(len(sg))

    print('\n'.join(wrap(''.join(sg), width=(sxn*(s+1)))))

    for sx,sy in product(range(minx,maxx+1),range(miny,maxy+1)):
        if (sx,sy) in simg:
            simd = simg[(sx,sy)]
            gd = data['tiles'][simd['tile_num']]
            grid = gd['grid']
            #grid = trans_copy(gd['grid'], s, s, *simd['transform'])
            for x,y in product(range(s),range(s)):
                xidx = (sx-minx)*(s+1)+x
                yidx = (sy-miny)*(s+1)+y

                sg[yidx*(s+1)*sxn+xidx] = grid[y*s+x]

    count = 0
    for line in wrap(''.join(sg), width=(sxn*(s+1))):
        print(line)
        count += 1
        if count > 0 and ( count % s == 0 ):
            print('') 
        

def print_prod(simg,ss):
    minx,miny = simg['min']
    maxx,maxy = simg['max']

    xlen = maxx-minx+1
    ylen = maxy-miny+1

    if xlen < ss or ylen < ss:
        print('WARNING: Super Image is only %s' % (str((xlen,ylen))) )

    prod = 1
    for coord in [(minx,miny),(minx,maxy),(maxx,miny),(maxx,maxy)]:
        if coord not in simg:
            print('WARNING: Corner %s Not In Super Image' % (str(coord)) )
        else:
            print("Corner: %s %s" % (simg[coord]['tile_num'],str(coord)) )
            prod *= simg[coord]['tile_num']

    print(str(prod) + '\n')

def update_bounds(simg,x,y):
    minx,miny = simg['min']
    maxx,maxy = simg['max']
    if x < minx:
        minx = x
    elif x > maxx:
        maxx = x
    if y < miny:
        miny = y
    elif y > maxy:
        maxy = y
    simg['min'] = (minx,miny)
    simg['max'] = (maxx,maxy)

def in_bounds(x,y,simg,ss):
    minx,miny = simg['min']
    maxx,maxy = simg['max']

    if x < minx:
        minx = x
    elif x > maxx:
        maxx = x
    if y < miny:
        miny = y
    elif y > maxy:
        maxy = y    

    return (maxx-minx+1) <= ss and (maxy-miny+1) <= ss

def on_boundary(x,y,simg,ss,dir):
    ox,oy = off[dir]
    return not in_bounds(x+ox,y+oy,simg,ss)

# clock-wise rotate from direction a to direction b in iterations of 90
def cw_rotates(a,b):
    ia = cwt[a]
    ib = cwt[b]
    return (ib-ia) % 4

def get_trans_edge_dir( facing, cwr, fwe, fns ):
    if fwe != fns:
        facing = opp[facing]
    return twc[(cwt[facing] + cwr) % 4]

# get permutations of all transformations for tile
# that will line up with passed direction
def get_possible_transforms(d,m):
    target_facing = opp[d]
    current_facing = m['dir']

    out = []

    # pure rotate
    cwrot_curr = cw_rotates(current_facing,target_facing)
    cwrot_opp = cw_rotates(opp[current_facing],target_facing)
    out.append([cwrot_curr,False,False])

    # flip y and rotate
    cwrot = cwrot_curr
    if current_facing == 'w' or current_facing == 'e':
        cwrot = cwrot_opp
    out.append([cwrot,False,True])

    # flip x and rotate
    cwrot = cwrot_curr
    if current_facing == 'n' or current_facing == 's':
        cwrot = cwrot_opp
    out.append([cwrot,True,False])

    # flip x and y and rotate
    out.append([cwrot_opp,True,True])

    return out

def trans_boundry(edge, facing, cwr, fwe, fns):

    # Flip
    ngrid = edge
    if ((fwe and facing == 'n' or facing == 's') or
        (fns and facing == 'w' or facing == 'e')):
        facing = opp[facing]

    if fwe != fns:
        ngrid = edge[::-1]

    # Rotate
    facing = twc[(cwt[facing]+cwr) % 4]

    return facing,ngrid

#   0 1 .. n           0 1 .. n  
# n +------+ 0       n +------+ 0
# . |      | 1  \ /  . |      | 1
# . |      | .  / \  . |      | .
# 1 |      | .       1 |      | .
# 0 +------- n       0 +------- n
#   n .. 1 0           n .. 1 0   
#
# Need to reverse one boundry to compare

# Make Sure Edges Shared With Any Placed Nodes Line Up!
# Transforms edges according to their transforms
def lines_up_with_neighbors( data, edges, simg, tile_num, x, y, cwr, fwe, fns ):
    gd = data['tiles'][tile_num]
    edges_match = True
    for edge in gd['edges']:
        mfacing,mgrid = trans_boundry(edge['edge'], edge['dir'], cwr, fwe, fns )

        ndir = opp[mfacing]
        ox,oy = off[mfacing]
        nx,ny = (x+ox,y+oy)
        if (nx,ny) in simg:
            simgd = simg[(nx,ny)]
            nd = data['tiles'][simgd['tile_num']]
            for nedge in nd['edges']:
                nfacing,ngrid = trans_boundry(nedge['edge'], nedge['dir'], *simgd['transform'] )
                if nfacing == ndir:
                    if ngrid != mgrid:
                        edges_match = False
                    break
    return edges_match

def add_to_sup_img( simg, tile_num, x, y, cwr, fwe, fns):
    simg[(x,y)] = {'tile_num' : tile_num, 'transform' : (cwr,fwe,fns)}
    simg['tiles'].add(tile_num)
    update_bounds(simg,x,y)

# 'grid' : trans_copy(gd['grid'],w,h,cwr,fwe,fns)
# simg = {'grid' : '...', 'tile_num' : XXXX, 'transform' : (cwr_in, fwe_in, fns_in) }
def stitch( data, edges, simg_in, tile_num_in, x_in, y_in, cwr_in, fwe_in, fns_in ):

    nodes = Queue()
    nodes.put( (simg_in, tile_num_in, x_in, y_in, cwr_in, fwe_in, fns_in) )

    ss = data['super_size']

    while not nodes.empty():
        simg, tile_num, x, y, cwr, fwe, fns = nodes.get()

        if end_program:
            print(simg)
            print_sgrid(simg)
            sys.exit(-1)

        gd = data['tiles'][tile_num]
        w,h = gd['width'],gd['height']

        most = 0

        add_to_sup_img( simg, tile_num, x, y, cwr, fwe, fns)

        # checks already made for tile placement
        # if we made it here and we've hit the total tiles
        # then we've solved the super image
        if len(simg['tiles']) == data['total_tiles']:
            print_image(data,simg,ss)
            print_prod(simg,ss)
            return True

        if most > len(simg['tiles']):
            most = len(simg['tiles'])

        could_place = False

        for edge in gd['edges']:
            edir = get_trans_edge_dir(edge['dir'], cwr, fwe, fns)
            if not on_boundary(x,y,simg,ss,edir): 

                # Find Matching Edges
                matching = edges.get(edge['edge'])
                if matching is None:
                    matching = edges.get(edge['edge'][::-1])
                    if matching is None:
                        continue

                for match in matching:
                    if match['tile_num'] == tile_num:
                        continue
                    ox,oy = off[edir]
                    nx,ny = (x+ox,y+oy)

                    # This Case Shouldn't Happen
                    if not in_bounds(nx,ny,simg,ss):
                        print('ERROR BAD COORDS')
                        sys.exit(-1)

                    if (nx,ny) not in simg:
                        transforms = get_possible_transforms(edir,match)
                        for cwr,fwe,fns in transforms:
                            if lines_up_with_neighbors(data, edges, simg, match['tile_num'], nx, ny, cwr, fwe, fns):
                                could_place = True
                                nodes.put( (copy.deepcopy(simg),match['tile_num'],nx,ny,cwr,fwe,fns) )


def part1(filename):
    data = read_grids(filename)
    atile = next(iter(data['tiles'].values())) 
    tw,th = atile['width'],atile['height']

    # group all edges in a dict 
    edges = {}
    for tile_num,gd in data['tiles'].items():
        tile_edges = get_edge_vec(gd)
        gd['edges'] = tile_edges
        for ed in tile_edges:
            if ed['edge'] in edges:
                edges[ed['edge']].append(ed)
            else:
                # Check Reversed Pattern
                redge = ed['edge'][::-1]
                if redge in edges:
                    edges[redge].append(ed)
                else:
                    edges[ed['edge']] = [ed]

    

    tile_num = 1427 #random.choices(list(data['tiles'].keys()))[0]

    print('Starting Tile: %d' % tile_num)

    stitch(data,edges,{'min': (0,0), 'max': (0,0), 'tiles' : set()},tile_num,0,0,0,False,False)

def part2(filename):
    data = read_grids(filename)

    #print(data)

end_program = False

def signal_handler(sig, frame):
    global end_program
    print('Aborting...')
    end_program = True

signal.signal(signal.SIGINT, signal_handler)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Solution to Advent of Code 2020 Day 20')
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