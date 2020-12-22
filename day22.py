import sys
import argparse
from pathlib import Path
import time
from collections import deque

def read_decks(filename):
    with open(filename) as fin:
        data_str = fin.read()
    sections = data_str.split('\n\n')
    d = []
    for s in sections:
        d.append(tuple([int(x) for x in s.rstrip().split('\n')[1:]]))
    return d

def new_deck( deck, n ):
    ndeck = deque(deck)

def play_recursive_combat( deck1, deck2, log_score ):
    deck1 = deque(deck1)
    deck2 = deque(deck2)
    configs = set()
    winner = -1

    while len(deck1) > 0 and len(deck2) > 0:

        t1 = tuple(deck1)
        t2 = tuple(deck2)

        if (t1,t2) in configs:
            if log_score:
                print_score(deck1)
            return 1

        configs.add((t1,t2))

        p1 = deck1.popleft()
        p2 = deck2.popleft()

        if p1 <= len(deck1) and p2 <= len(deck2):
            winner = play_recursive_combat( tuple(deck1)[:p1], tuple(deck2)[:p2], False )
        else:
            winner = 1 if p1 > p2 else 2

        if winner == 1:
            deck1.append(p1)
            deck1.append(p2)
        else:
            deck2.append(p2)
            deck2.append(p1)

    winner = 2 if len(deck1) == 0 else 1

    if log_score:
        print_score(deck1 if winner == 1 else deck2)

    return winner

def print_score( deck ):
    dl = len(deck)
    print( sum([(dl-i)*x for i,x in enumerate(deck)]) )

def part1(filename):
    deck1,deck2 = read_decks(filename)

    deck1 = deque(deck1)
    deck2 = deque(deck2)

    while len(deck1) > 0 and len(deck2) > 0:
        p1 = deck1.popleft()
        p2 = deck2.popleft()

        if p1 > p2:
            deck1.append(p1)
            deck1.append(p2)
        else:
            deck2.append(p2)
            deck2.append(p1)

    wd = deck2 if len(deck1) == 0 else deck1
    print_score(wd)

def part2(filename):
    deck1,deck2 = read_decks(filename)

    play_recursive_combat(deck1,deck2,True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Solution to Advent of Code 2020 Day 22')
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