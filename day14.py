import sys
import argparse
from pathlib import Path
import re
from itertools import permutations
import time

mem_re = re.compile('mem\[([0-9]+)\] = ([0-9]+)')

def addmask( mask ):
    return int(mask.replace('X','0'),2)

def submask( mask ):
    return int(mask.replace('X','1'),2)

def assign_with_masked_value( mask, hm, key, value ):
    hm[key] = (value | addmask(mask)) & submask(mask)

def assign_with_masked_address(mask, hm, key, value):
    count = mask.count('X')
    base_address = key & int(mask.replace('0','1').replace('X','0'),2)
    float_bits = [i for i,v in enumerate(mask) if v == 'X']
    for perm in range(2**count):
        address_mask = list(mask)
        for i,b in zip(float_bits,bin(perm)[2:].zfill(count)):
            address_mask[i] = b
        address_mask = int(''.join(address_mask),2)
        hm[base_address | address_mask] = value

def read_program(filename):
    lines = []
    with open(filename) as fin:
        for line in fin:
            if line.startswith('mask'):

                lines.append( ( 'mask',(line.rstrip().split(' = ')[1],)) )
            elif line.startswith('mem'):
                m = mem_re.match(line)
                if m:
                    address = int(m.group(1))
                    value = int(m.group(2))
                    lines.append(('assign',(address,value)))

    return lines

def get_init_code(filename):
    program = read_program(filename)

    mask = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
    hm = {}

    for op,args in program:
        if op == 'mask':
            mask = args[0]
        elif op == 'assign':
            assign_with_masked_value( mask, hm, args[0], args[1] )

    print(sum(hm.values()))

def func(filename):
    program = read_program(filename)

    mask = '000000000000000000000000000000000000'
    hm = {}

    for op,args in program:
        if op == 'mask':
            mask = args[0]
        elif op == 'assign':
            assign_with_masked_address( mask, hm, args[0], args[1] )    

    print(sum(hm.values()))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Solution to Advent of Code 2020 Day 14')
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
            get_init_code(args.file)
        else:
            func(args.file)
        end = time.time()
        print( "%f ms" % ((end-start)*1000))