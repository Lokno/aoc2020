from lark import Lark
from pathlib import Path
import string
import re
import time
import argparse

def day20_Grammer( filename, part ):
    rule_11_re = re.compile('(?<!\d)11: .*\n')
    rule_08_re = re.compile('(?<!\d)8: .*\n')

    with open(filename) as fin:
        file_str = fin.read()

    file_str,input_str = file_str.split('\n\n')

    if part == 2:
        file_str = rule_11_re.sub('11: 42 31 | 42 11 31\n', file_str)
        file_str = rule_08_re.sub('8: 42 | 42 8\n', file_str)

    for c in string.digits:
        file_str = file_str.replace(c,chr( ord(c)-ord('0')+ord('a') ))

    file_str = 'start: a\n' + file_str

    print(file_str)

    day19_rules = Lark(file_str)

    count = 0
    for line in input_str.split('\n'):
        try:
            out = day19_rules.parse(line)
            count += 1
        except:
            pass

    print(count)

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
        day20_Grammer(args.file,args.part)
        end = time.time()
        print( "%f ms" % ((end-start)*1000))