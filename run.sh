#!/bin/bash

if { [ $# -gt 0 ] && [[ ! $1 =~ ^[0-9]+$ ]]; } || 
   { [ $# -eq 1 ] && [[ ! $1 =~ ^[1-2]$ ]]; } ||
   { [ $# -gt 1 ] && [[ ! $2 =~ ^[1-2]$ ]]; };
then
    echo "   usage $0 [<day 1-25> = Today] [<part 1,2> = 1]"
    exit 1;
fi
part=1
day=$(date -d "$D" '+%d')
if [ $# -eq 1 ];
then
    part=$1
elif [ $# -eq 2 ];
then
    printf -v day "%02d" $1
    part=$2
fi

echo python day${day}.py input/day${day}_input.txt --part $part
python day${day}.py input/day${day}_input.txt --part $part