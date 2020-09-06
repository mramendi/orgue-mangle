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
    print("Usage: "+sys.argv[0]+" infile outfile seconds_to_cut_from_start")
    exit(1)
inputLines=open(sys.argv[1]).readlines()
millisecondsToCut=int(sys.argv[3])*1000
service_tst=0
prev_command_tst=0
cutReached=False
actualStart=0

for cline in inputLines:
    tst=tStamp(cline)
    if tst==0:
        outputLines.append(cline)
        continue
    if tst<100:
        service_tst=tst 
        outputLines.append(cline)
        continue
        
    cmd=commandName(cline)
    
    if tst<millisecondsToCut:
        # drop all note on/note off
        if cmd in ["On","Off"]:
            continue
        
        # this is a service command. Put it at the service timestamp
        # but if the previous command original timestamp was not the same as this one's.
        # then increase the service timestamp by 1 first
        
        if tst != prev_command_tst:
            service_tst += 1
            prev_command_tst = tst
        outputLines.append(cline.replace(str(tst),str(service_tst)))
        
        continue
        
    # If we reached here, then the timestamp above the cut was reached
    if not cutReached:
        cutReached=True
        print(cline)
        actualStartSec=((service_tst+1)//1000)+1
        actualStart=actualStartSec*1000
        print("Actual start is",actualStartSec," seconds")
        print("To convert timestamps, add",int(sys.argv[3])-actualStartSec," seconds")
        
    # change and replace the timestamp, save line to output
    new_tst=tst-millisecondsToCut+actualStart
    outputLines.append(cline.replace(str(tst),str(new_tst)))
    
open(sys.argv[2],"w").writelines(outputLines)
    


