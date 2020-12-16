import sys
import argparse
from pathlib import Path
import re
from itertools import chain

line_re = re.compile("([a-z ]+): ([0-9]+)-([0-9]+) or ([0-9]+)-([0-9]+)")

hdl_comma = lambda line: [int(x) for x in line.split(',')]
hdl_regex = lambda line: line_re.match(line).groups() if line_re.match(line) else ()

def read_lines(lines, handler):
    return [handler(line.rstrip()) for line in lines]

def read_data(filename):
    data = {}
    with open(filename) as fin:
        data_str = fin.read()

    sections = data_str.split('\n\n')

    data['fields'] = read_lines(sections[0].split('\n'),hdl_regex)
    data['your_ticket'] = hdl_comma(sections[1].split('\n')[1])
    data['nearby_tickets'] = read_lines(sections[2].rstrip().split('\n')[1:],hdl_comma)

    return data

def valid_fields(x,fields):
    valid = []
    for name, sa, ea, sb, eb in fields:
        if int(sa) <= x <= int(ea) or int(sb) <= x <= int(eb):
            valid.append(name)
    return valid

def sum_invalid_values(filename):
    data = read_data(filename)

    fc = len(data['your_ticket'])

    invalid = 0

    for ticket in data['nearby_tickets']:
        for i in range(fc):
            if len(valid_fields(ticket[i],data['fields'])) == 0:
                invalid += ticket[i]
                break

    print(invalid)

def remove_invalid_tickets(data):
    fc = len(data['your_ticket'])
    new_list = []
    for ticket in data['nearby_tickets']:
        valid = True
        for i in range(fc):
            if len(valid_fields(ticket[i],data['fields'])) == 0:
                valid = False
                break
        if valid:
            new_list.append(ticket)

    data['nearby_tickets'] = new_list

def determine_fields(filename):
    data = read_data(filename)
    fc = len(data['your_ticket'])

    remove_invalid_tickets(data)

    fs = set([name for name, sa, ea, sb, eb in data['fields']])

    possible = []

    for i in range(fc):
        ps = set(fs)
        for ticket in chain([data['your_ticket']],data['nearby_tickets']):
            ps.intersection_update(set(valid_fields(ticket[i],data['fields'])))

        nps = fs.difference(ps)
        possible.append(ps)

    fields = [None] * fc

    while None in fields:

        for i,ps in enumerate(possible):
            if len(ps) == 1:
                fields[i] = ps.pop()

        for i,field in enumerate(fields):
            if field is None:
                continue

            for j in range(fc):
                if i != j:
                    if field in possible[j]:
                        possible[j].remove(field)

    prod = 1

    for i,field in enumerate(fields):
        if field.startswith('departure'):
            prod *= data['your_ticket'][i]

    print(prod)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Solution to Advent of Code 2020 Day 16')
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
            sum_invalid_values(args.file)
        else:
            determine_fields(args.file)