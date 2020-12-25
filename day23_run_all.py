# Divides up <count> lines from the <input> file between some number of <threads> 

import os,sys
import subprocess

if len(sys.argv) < 5:
    print(" %s <input> <output prefix> <count> <threads>" % sys.argv[0])
    sys.exit(-1)

cmd = "./day23 %s %d"

input_file = sys.argv[1]
output_prefix = sys.argv[2]
count = int(sys.argv[3])
threads = int(sys.argv[4])

count_per = int(count / threads)

print("Running day23 calculating %d results on %d threads (%d each)..." % (count,threads,count_per))

for i in range(threads):
    cmd = "python day23_run_block.py %s %s %d %d &"
    cmd = cmd % (input_file,output_prefix+str(i+1).zfill(3)+'.txt',i*count_per+1,count_per)
    os.system(cmd)