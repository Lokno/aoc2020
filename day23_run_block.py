# Executes day23 code for an entire block of input, and saves the results to a csv file

import os,sys
import subprocess

if len(sys.argv) < 5:
    print(" %s <input> <output> <start> <count>" % sys.argv[0])
    sys.exit(-1)

cmd = "./day23 %s %d"

input_file = sys.argv[1]
output_file = sys.argv[2]
start = int(sys.argv[3])
count = int(sys.argv[4])

with open(input_file) as fin:
    inputs = fin.readlines()[start-1:start-1+count]

print("Running day23 for inputs %d through %d..." % (start,start+count))

with open(output_file,"w") as fout:

    for i in inputs:
        seq = i.rstrip()
        line = seq

        process = subprocess.Popen(['./day23', seq, '1'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = process.communicate()

        line += ',' + out.decode("utf-8").rstrip()

        process = subprocess.Popen(['./day23', seq, '2'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = process.communicate()

        line += ',' + out.decode("utf-8")

        fout.write(line)