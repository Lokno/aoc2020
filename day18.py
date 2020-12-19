import sys
import argparse
from pathlib import Path
import re
import time

inparam_re = re.compile("\(([^\(\)]+)\)")
simple_re = re.compile("( [*+] |[0-9]+)")

def read_lines(filename):
    with open(filename) as fin:
        data = [line.rstrip() for line in fin ]
    return data

def read_grid(filename):
    data = {}

    with open(filename) as f:
        grid = f.read()

    data['height'] = grid.count('\n')
    data['width'] = grid.find('\n')
    data['grid'] = grid.replace('\n', '')

    return data

def read_grouped_data(filename, wraps, handler):
    data = []
    with open(filename) as fin:
        data_str = fin.read()

    entries = data_str.split('\n\n')

    for entry in entries:
        if wraps:
            data.append(handler(entry.rstrip().replace('\n',' ')))
        else:
            data.append([handler(item) for item in entry.rstrip().split('\n')])

    return data

def solve_basic(eq):
    result = 0
    first = True
    op = None
    for token in simple_re.findall(eq):
        if first:
            first = False
            result = int(token)
        elif op is None:
            op = token.strip()
        else:
            result = result*int(token) if op == '*' else result+int(token)
            op = None

    return result

def solve_equation(eq):
    groups = inparam_re.findall(eq)
    while groups:
        for params in groups:
            eq = eq.replace('('+params+')',str(solve_basic(params)))
        groups = inparam_re.findall(eq)
    return solve_basic(eq)

def solve_advanced(eq):
    tokens = simple_re.findall(eq)
    while ' + ' in tokens:    
        idx = tokens.index(' + ')
        result = int(tokens[idx-1]) + int(tokens[idx+1])
        tokens = tokens[:idx-1] + [str(result)] + tokens[idx+2:]

    return solve_basic(''.join(tokens))

def solve_equation_advanced(eq):
    groups = inparam_re.findall(eq)
    while groups:
        for params in groups:
            eq = eq.replace('('+params+')',str(solve_advanced(params)))
        groups = inparam_re.findall(eq)
    return solve_advanced(eq)

def part1(filename):
    equations = read_lines(filename)
    print(sum([solve_equation(eq) for eq in equations]))


def part2(filename):
    equations = read_lines(filename)
    print(sum([solve_equation_advanced(eq) for eq in equations]))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Solution to Advent of Code 2020 Day 18')
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