import sys
import argparse
from pathlib import Path
from queue import Queue

def read_values(filename):
    with open(filename) as fin:
        values = [int(v) for v in fin]
    return values

def get_adapters_within_tolerance(voltage,adapters):
    valid = []
    for a in adapters:
        delta = a-voltage 
        if 1 <= delta <= 3:
            valid.append(a)
        if delta > 3:
            break

    return valid

def use_every_adapter(filename):
    adapters = read_values(filename)
    adapters.sort()
    device_voltage_rating = adapters[-1]+3

    voltage = 0

    sums = [0,0,0]

    while (device_voltage_rating-voltage) > 3:
        valid_adapters = get_adapters_within_tolerance(voltage,adapters)

        if len(valid_adapters) == 0:
            print('ERROR: no adapter found to continue chain')
            sys.exit(-1)

        avolt = valid_adapters[0]

        delta = avolt-voltage
        sums[delta-1] += 1
        voltage = avolt

    delta = device_voltage_rating-voltage
    sums[delta-1] += 1

    print(sums[0]*sums[2])

def count_arrangements_from(adapters,voltage,known,device_voltage_rating):
    adapters = [a for a in adapters if a > voltage]
    
    q = Queue()
    q.put((voltage,adapters))

    arrangements = 0

    while not q.empty():
        state = q.get()

        if (device_voltage_rating-state[0]) <= 3:
            arrangements += 1
        elif state[0] in known:
            arrangements += known[state[0]]
        else:
            valid_adapters = get_adapters_within_tolerance(state[0],state[1])
            for a in valid_adapters:
                new_list = list(state[1])
                new_list.remove(a)
                q.put( (a,new_list) )

    known[voltage] = arrangements

    return arrangements



def count_arrangements(filename):
    adapters = read_values(filename)
    adapters.sort()
    device_voltage_rating = adapters[-1]+3

    known = {}

    for i in range(len(adapters)-1,0,-1):
        count_arrangements_from(adapters,adapters[i],known,device_voltage_rating)
        
    print(count_arrangements_from(adapters,0,known,device_voltage_rating))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Solution to Advent of Code 2020 Day 10')
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
            use_every_adapter(args.file)
        else:
            count_arrangements(args.file)