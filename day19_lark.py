from lark import Lark
from num2words import num2words
from pathlib import Path
import re
import time
import argparse

def day20_Grammer( filename, part ):
    rule_11_re = re.compile('(?<!_)eleven: .*\n')
    rule_08_re = re.compile('(?<!_)eight: .*\n')

    with open(filename) as fin:
        file_str = fin.read()

    file_str,input_str = file_str.split('\n\n')

    # create letter names
    d = {}
    for line in file_str.split('\n'):
        num = int(line.split(':')[0])
        d[num] = num2words(num).replace('-','_').replace(' ','_')

    dict_list = list(d.items())
    dict_list.sort(reverse=True, key = lambda x : x[0])

    for idx,name in dict_list:
        file_str = file_str.replace(str(idx),name)

    file_str = 'start: %s\n\n' % d[0] + file_str

    if part == 2:
        file_str = rule_11_re.sub('eleven: forty_two thirty_one | forty_two eleven thirty_one\n', file_str)
        file_str = rule_08_re.sub('eight: forty_two | forty_two eight\n', file_str)

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