#!/usr/bin/python3

import sys

outputLines=[]

def tStamp(line):
    spl=line.split()
    try:
        return int(spl[0])
    except ValueError:
        return 0
        
def commandName(line):
    spl=line.split()
    try:
        return spl[1]
    except IndexError:
        return ""

if len(sys.argv)!=5:
    print("Usage: "+sys.argv[0]+" infile outfile start shift")
    exit(1)
inputLines=open(sys.argv[1]).readlines()
start=int(sys.argv[3])
shift=int(sys.argv[4])

if start<1:
    start=1
    print("WARNING: start set to 1")
    
last_timestamp=0

for cline in inputLines:
    tst=tStamp(cline)
    if tst<start:
        outputLines.append(cline)
        if tst>last_timestamp:
            last_timestamp=tst
        continue
    new_tst=tst+shift
    if new_tst<last_timestamp:
        print("WARNING: non-sequential time stamp",new_tst)
    outputLines.append(cline.replace(str(tst),str(new_tst),1))
    
open(sys.argv[2],"w").writelines(outputLines)
    


