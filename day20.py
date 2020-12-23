import argparse
from pathlib import Path
from itertools import product,permutations
from collections import deque
import sys,math,time

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
            ia = y*w+x
            ib = (h-1-y)*w+x
            tmp = grid[ia]
            grid[ia] = grid[ib]
            grid[ib] = tmp

    return grid

# assumes grid is square
def rotate_grid( grid, s, cw_rot ):
    if cw_rot == 0:
        return grid

    ngrid = list(grid)
    ngrid2 = list(grid)
    for i in range(cw_rot):
        for x,y in product(range(s),range(s)):
            nx = y
            ny = s-1-x
            ngrid2[ny*s+nx] = ngrid[y*s+x]
        tmp = ngrid
        ngrid = ngrid2
        ngrid2 = tmp

    return ngrid

def strip_border( grid, w, h ):
    ngrid = []
    for y in range(1,h-1):
        ngrid += grid[w*y+1:w*(y+1)-1]
    return ngrid

def trans_copy(grid, w, h, cwr, fwe, fns):
    grid = flip_grid( list(grid), w, h, fwe, fns )
    grid = rotate_grid( grid, w, cwr )
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

def build_image( data, simg, ss, borders, flipy ):
    minx,miny = simg['min']
    maxx,maxy = simg['max']

    s = data['size']
    sb = s

    if not borders:
        sb -= 2
        s -= 2

    sxn = (maxx-minx+1)
    syn = (maxy-miny+1)

    sg = [' '] * sxn * syn * sb * sb

    for sx,sy in product(range(minx,maxx+1),range(miny,maxy+1)):
        if (sx,sy) in simg:

            simd = simg[(sx,sy)]
            gd = data['tiles'][simd['tile_num']]
            grid = gd['grid']

            if not borders:
                grid = trans_copy(grid, s+2, s+2, *simd['transform'])
            else:
                grid = trans_copy(grid, s+2, s+2, *simd['transform'])

            if not borders:
                grid = strip_border(grid,s+2,s+2)

            for x,y in product(range(s),range(s)):
                xidx = (sx-minx)*sb+x
                yidx = (sy-miny)*sb+y

                # need to flip y for printing
                if flipy:
                    yidx = sb*syn-1-yidx
                    sg[yidx*sb*sxn+xidx] = grid[(s-1-y)*s+x]
                else:
                    sg[yidx*sb*sxn+xidx] = grid[y*s+x]

    return sg

def count_matches( grid, gw, gh, temp, char, tw, th):
    matches = 0
    twh = int(tw/2)
    thh = int(th/2)
    coords = [(x,y) for x,y in product(range(tw),range(th)) if temp[tw*y+x] == char]
    for x,y in product(range(gw-tw),range(gh-th)):
        count = 0
        for tx,ty in coords:
            nx = x+tx
            ny = y+ty
            if grid[ny*gw+nx] == char:
                count += 1
        if count == len(coords):
            for tx,ty in coords:
                nx = x+tx
                ny = y+ty
                grid[ny*gw+nx] = 'O'
            matches += 1
    return matches

def print_image_with_stats( data, simg, ss, borders ):
    minx,miny = simg['min']
    maxx,maxy = simg['max']

    s = data['size']
    sb = s

    if not borders:
        sb -= 2
        s -= 2

    sxn = (maxx-minx+1)
    syn = (maxy-miny+1)

    sg = build_image( data, simg, ss, borders, True )

    sm = """
                   # 
 #    ##    ##    ###
  #  #  #  #  #  #   
"""

    smd = read_grid(sm[1:-1])

    most_sm = 0
    most_grid = ''

    for cwr,fwe,fns in product( range(4), [False,True], [False,True] ):
        sgc = trans_copy(sg,sxn*s,syn*s,cwr,fwe,fns)

        count = count_matches(sgc,sxn*s,syn*s,smd['grid'],'#',smd['width'],smd['height'])

        if count > most_sm:
            most_sm = count
            most_grid = sgc

    grid_str = ''.join(most_grid)
    hash_count = sg.count('#')

    lines = wrap(''.join(grid_str), width=(sxn*sb))
    count = 0
    for line in lines:
        count += 1
        print(line)

    print('\nSea Monsters:    %d' % most_sm )
    print("'#' Count:       %d" % hash_count)
    print("Water Roughness: %d\n" % (hash_count-most_sm*15))

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

# relative to bottom-left corner
def in_bounds_bl_corner(x,y,cx,cy,ss):
    return cx <= x < ss and cy <= y < ss

def trans_boundry(edge, facing, cwr, fwe, fns):

    # Flip
    ngrid = edge
    if ((fwe and (facing == 'w' or facing == 'e')) or
        (fns and (facing == 'n' or facing == 's'))):
        facing = opp[facing]

    if fwe != fns:
        ngrid = edge[::-1]

    facing = twc[(cwt[facing]-cwr) % 4]

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
# Make sure the edges line up!
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
                    if ngrid != mgrid[::-1]:
                        edges_match = False
                        break
        if not edges_match:
            break

    return edges_match

def add_to_sup_img( simg, tile_num, x, y, cwr, fwe, fns):
    simg[(x,y)] = {'tile_num' : tile_num, 'transform' : (cwr,fwe,fns)}
    simg['tiles'].add(tile_num)
    update_bounds(simg,x,y)

def gather_corners(data, edges):
    corners = []
    for tile_num,gd in data['tiles'].items():
        uniques = []
        for edge in gd['edges']:
            matching = edges.get(edge['edge'])
            if matching is None:
                matching = edges.get(edge['edge'][::-1])

            if matching is None:
                print('this shouldn\'t happen')
                uniques.append(edge['dir'])
            elif len(matching) == 1 and matching[0]['tile_num'] == tile_num:
                uniques.append(edge['dir'])
        if len(uniques) > 1:
            corners.append((tile_num,uniques))

    return corners

# Start with a corner piece in the bottom left
# For each open spot in a NSWE direction from a filled tiles
# Find a valid tile that fits the edges at that position
# Repeat until the entire super image is filled

def stitch( data, edges, simg, bl_tile_num, bl_x, bl_y, bl_cwr, bl_fwe, bl_fns ):
    ss = data['super_size']

    add_to_sup_img( simg, bl_tile_num, bl_x, bl_y, bl_cwr, bl_fwe, bl_fns)

    open_spots = set([(0,1),(1,1),(1,0)])

    dirs = ((-1, 0), (0, -1), (0, 1), (1, 0))

    unused_tiles = set([tn for tn in data['tiles'].keys() if tn != bl_tile_num])

    while len(open_spots) > 0:

        spots_filled = set()

        for x,y in open_spots:
            could_fill = False
            for tile in unused_tiles:
                for cwr,fwe,fns in product(range(4),[True,False],[True,False]):
                    if lines_up_with_neighbors(data, edges, simg, tile, x, y, cwr, fwe, fns):
                        if not could_fill:
                            could_fill = True
                            spots_filled.add((x, y))
                            add_to_sup_img( simg, tile, x, y, cwr, fwe, fns)
                            unused_tiles.remove(tile)
                            break
                if could_fill:
                    break

        if len(open_spots) == len(spots_filled):
            open_spots = set()
            for spot in spots_filled:
                simgd = simg[spot]
                x,y = spot
                gd = data['tiles'][simgd['tile_num']]
                for ox,oy in dirs:
                    nx,ny = (x+ox,y+oy)
                    if (nx,ny) not in simg and (nx,ny) not in spots_filled and (nx,ny) not in open_spots and in_bounds_bl_corner(nx,ny,bl_x,bl_y,ss):
                        open_spots.add((nx,ny))
        else:
            print("Could not fill all open spots")
            break

    print_image_with_stats(data,simg,ss,False)

def gather_edges( data ):
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
    return edges

def product_of_corner_tiles(filename):
    data = read_grids(filename)
    edges = gather_edges(data)
    corners = gather_corners(data, edges)

    prod = 1
    for tile_num,uniques in corners:
        prod *= tile_num

    print(prod)

def find_sea_monsters(filename):
    data = read_grids(filename)
    edges = gather_edges(data)
    corners = gather_corners(data, edges)

    ss = data['super_size']

    simgd = {'min': (0,0), 'max': (0,0), 'tiles' : set()}

    tile_num = 0
    borders = []

    for tn,b in corners:
        b.sort()
        if ''.join(b) == 'es':
            tile_num = tn
            borders = b

    stitch(data,edges,simgd,tile_num,0,0,0,False,False)

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
            product_of_corner_tiles(args.file)
        else:
            find_sea_monsters(args.file)
        end = time.time()
        print( "%f ms" % ((end-start)*1000))