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

if len(sys.argv)!=4:
    print("Usage: "+sys.argv[0]+" infile outfile shift")
    exit(1)
inputLines=open(sys.argv[1]).readlines()
shift=int(sys.argv[3])

for cline in inputLines:
    tst=tStamp(cline)
    if tst==0:
        outputLines.append(cline)
        continue
    new_tst=tst+shift
    outputLines.append(cline.replace(str(tst),str(new_tst),1))
    
open(sys.argv[2],"w").writelines(outputLines)
    


