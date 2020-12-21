import sys
import argparse
from pathlib import Path
import re
import time

line_re = re.compile("(.*) \(contains ([^\)]+)\)")

hdl_regex = lambda line: line_re.match(line).groups() if line_re.match(line) else ()

def read_lines(filename, handler):
    with open(filename) as fin:
        data = [handler(line.rstrip()) for line in fin ]
    return data

def resolve_allergens(data):
    d = {}

    # gather candidate ingredients
    for entry in data:
        words = set(entry[0].split(' '))
        allergens = set(entry[1].split(', '))
        for a in allergens:
            if a in d:
                d[a].intersection_update(words)
            else:
                d[a] = set(words)

    # resolve allergens
    change = True
    while change:
        change = False
        for name,words in d.items():
            if len(words) == 1:
                w = next(iter(words))
                for nameb,wordsb in d.items():
                    if len(wordsb) > 1 and w in wordsb:
                        change = True
                        wordsb.discard(w)

    return d

def part1(filename):
    data = read_lines(filename,hdl_regex)

    resolve_allergens(data)

    hypoallergenic = set()

    # Get set of non-allergic ingredients
    for entry in data:
        words = set(entry[0].split(' '))
        for allergen,ingredients in d.items():
            i = next(iter(ingredients))
            if i in words:
                words.remove(i)
        hypoallergenic.update(words)

    total_count = 0

    for ingredient in hypoallergenic:
        for entry in data:
            total_count += entry[0].split(' ').count(ingredient)

    print(total_count)

def part2(filename):
    data = read_lines(filename,hdl_regex)

    d = resolve_allergens(data)

    allergens = [(a,next(iter(i))) for a,i in d.items()]
    allergens.sort(key=lambda x: x[0])
    print(','.join([i for a,i in allergens]))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Solution to Advent of Code 2020 Day 21')
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