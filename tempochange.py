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

if not len(sys.argv) in [4,5,6]:
    print("Usage: "+sys.argv[0]+" infile outfile percentage [start [end]]")
    exit(1)
inputLines=open(sys.argv[1]).readlines()

tempo_change = int(sys.argv[3])/100

try:
    start=int(sys.argv[4])
    if start<100:
        print ("WARNING: Assuming start at 100 ms")
        start = 100
except IndexError: start=100

try:
    end=int(sys.argv[5])
    if end<=start:
        print ("ERROR: End position is not after start position")
        exit(1)
except IndexError: end=1000*60*60*24*1000 # a thousand days in milliseconds; no MIDI recording should be this long
    

changed_part_started = False
first_timestamp_of_changed_part = 0

# The shift value is calculates as the value by which the last timestamp of the changed part was shifted
shift_value_after_changed_part = 0

for cline in inputLines:
    tst=tStamp(cline)
    
    if tst<start:
        outputLines.append(cline)
        continue
    
    # At this point we are at least beyond the start
    if not changed_part_started:
        if tst>end:
            print("ERROR: No MIDI events between start and end")
            exit(1)
        changed_part_started=True
        first_timestamp_of_changed_part=tst 
        outputLines.append(cline)
        continue

    if tst<=end:
        # we are in the changed part and the first timestamp is already recorded
        # so change the time from that first timestamp to current timestamp according to tempo change
        time_diff = tst-first_timestamp_of_changed_part
        new_tst = round(first_timestamp_of_changed_part+(time_diff*tempo_change))
        shift_value_after_changed_part = new_tst-tst
        outputLines.append(cline.replace(str(tst),str(new_tst),1))
    else:
        # we are past the end position
        new_tst = tst+shift_value_after_changed_part
        outputLines.append(cline.replace(str(tst),str(new_tst),1))
    
open(sys.argv[2],"w").writelines(outputLines)
    


