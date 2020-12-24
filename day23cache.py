import sys,string

if len(sys.argv) < 3:
    print("  usage %s <sequence> <part 1,2>" % sys.argv[0])
    sys.exit(-1)

seq,part = sys.argv[1:3]

if len(seq) != 9 or len(seq) != len(set(seq)) or any([s not in string.digits[1:] for s in seq]):
    print('Invalid Sequence: %s' % (seq))
else:
    found = False
    with open("day23_all_answers.csv") as fin:
        for row in fin:  
            if not row.startswith(seq):
                continue
            else:
                s,p1,p2 = row.rstrip().split(',')
                found = True
                print( p1 if part == '1' else p2 )
    if found == False:
        print('...uh')