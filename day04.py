import sys
import argparse
import re
from pathlib import Path
import time

required_re = re.compile('(ecl|pid|eyr|hcl|byr|iyr|hgt)')

byr_re = re.compile('byr:([0-9]+)')
iyr_re = re.compile('iyr:([0-9]+)')
eyr_re = re.compile('eyr:([0-9]+)')
hgt_re = re.compile('hgt:([0-9]+)(cm|in)')
hcl_re = re.compile('hcl:#([0-9a-f]+)')
ecl_re = re.compile('ecl:(amb|blu|brn|gry|grn|hzl|oth)')
pid_re = re.compile('pid:([0-9]+)')

def count_required(filename):
    with open(filename) as fin:
        data_str = fin.read()

    entries = data_str.split('\n\n')

    valid = 0
    for entry in entries:
        if len(required_re.findall(entry)) == 7:
            valid += 1

    print(valid)

def check_hgt( value, unit ):
    if unit == 'cm':
        return 150 <= value <= 193
    else:
        return 59  <= value <= 76

def count_required_and_valid(filename):
    with open(filename) as fin:
        data_str = fin.read()

    entries = data_str.split('\n\n')

    valid = 0
    for entry in entries:
        byr_m = byr_re.findall(entry)
        iyr_m = iyr_re.findall(entry)
        eyr_m = eyr_re.findall(entry)
        hgt_m = hgt_re.findall(entry)
        hcl_m = hcl_re.findall(entry)
        ecl_m = ecl_re.findall(entry)
        pid_m = pid_re.findall(entry)

        if( len(byr_m) and len(iyr_m) and len(eyr_m) and 
            len(byr_m[0]) == 4 and len(iyr_m[0]) == 4 and len(eyr_m[0]) == 4 and 
            len(hgt_m) and len(hcl_m) and len(hcl_m[0]) == 6 and
            len(ecl_m) and len(pid_m) and len(pid_m[0]) == 9 and
            (1920 <= int(byr_m[0]) <= 2002) and
            (2010 <= int(iyr_m[0]) <= 2020) and
            (2020 <= int(eyr_m[0]) <= 2030) and
            check_hgt(int(hgt_m[0][0]), hgt_m[0][1])):
            valid += 1

    print(valid)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Solution to Advent of Code 2020 Day 04')
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
            count_required(args.file)
        else:
            count_required_and_valid(args.file)
        end = time.time()
        print( "%f ms" % ((end-start)*1000))