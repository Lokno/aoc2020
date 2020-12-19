import sys
import argparse
import re
from pathlib import Path
from queue import Queue
import time

line_re     = re.compile('(\w+) (\w+) bags contain (.*)')
contents_re = re.compile('(\d+) (\w+) (\w+) bags?')

def read_bag_rules(filename):
    bags = {}
    with open(filename) as fin:
        for line in fin:
            m = line_re.match(line)
            if m:
                adj,col,content_str = m.groups()
                contents = contents_re.findall(content_str)
                bags[adj + ' ' + col] = {'adj' : adj, 'col' : col, 'contents' : contents }
    return bags

def count_bags_that_contain_target(filename,target_name):
    bags = read_bag_rules(filename) 
    count = 0

    for bag in bags.keys():

        if bag == target_name:
            continue

        bags_to_check = Queue()
        bags_to_check.put(bag)

        target_found = False

        while not bags_to_check.empty():
            parent_bag = bags_to_check.get()
            if parent_bag == target_name:
                target_found = True
                break
            else:
                for child_bag in bags[parent_bag]['contents']:
                    bag_name = child_bag[1] + ' ' + child_bag[2]
                    bags_to_check.put(bag_name)
                    

        if target_found:
            count += 1

    print(count)

def total_required_bags_in_bag(filename,target_name):
    bags = read_bag_rules(filename) 
    count = 0
    bags_to_check = Queue()
    bags_to_check.put({ 'name' : target_name, 'count' : 1 })
    target_found = False

    while not bags_to_check.empty():
        parent_data = bags_to_check.get()
        if parent_data['name'] != target_name:
            count += parent_data['count']

        for child_bag in bags[parent_data['name']]['contents']:
            bag_name = child_bag[1] + ' ' + child_bag[2]
            bags_to_check.put( { 'name' : bag_name, 'count' : int(child_bag[0])*parent_data['count'] } )
                
    print(count)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Solution to Advent of Code 2020 Day 07')
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
            count_bags_that_contain_target(args.file,'shiny gold')
        else:
            total_required_bags_in_bag(args.file,'shiny gold')
        end = time.time()
        print( "%f ms" % ((end-start)*1000))