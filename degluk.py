#!/usr/bin/python3

import types
import sys

outputLines=[]
notesInProgress={}
chatterLimit=30 # in milliseconds

def tStamp(line):
    spl=line.split()
    try:
        return int(spl[0])
    except ValueError:
        return 0
    
    
#    ts=""
#    i=0
#    try:
#        while line[i].isnumeric():
#            ts+=line[i]
#            i+=1
#    except IndexError: pass
#    if ts=="":
#        return 0
#    else:
#        return int(ts)
        
def noteName(line):
    spl=line.split()
    nt=""
    ch=""
    for piece in spl:
        if (piece.find("n=")==0) or (piece.find("note=")==0):
            nt=piece.split("=")[1]
        if (piece.find("ch=")==0):
            ch=piece.split("=")[1]
    if (nt=="") or (ch==""):
        raise ValueError("Failed to parse note: "+line)
    return ch+"_"+nt
    
def commandName(line):
    spl=line.split()
    try:
        return spl[1]
    except IndexError:
        return ""
        
def addToOutput(line):
    tst=tStamp(line)
    if outputLines==[] or tst==0:
        outputLines.append(line)
        return
    idx=len(outputLines)
    while (tStamp(outputLines[idx-1])>tst) and (idx>0):
        idx-=1
    outputLines.insert(idx,line)
    return
    
if len(sys.argv)!=3:
    print("Usage: "+sys.argv[0]+" infile outfile")
    exit(1)
inputLines=open(sys.argv[1]).readlines()

for cline in inputLines:
    
    cmd=commandName(cline)
    if not cmd in ["On","Off","Meta"]:
        addToOutput(cline)
        continue
    tst=tStamp(cline)
    
    # Move existing saved note changes to output (unless cancelled by chatter) if 20 ms have passed or if the command is Meta
    # Note: we rely on Meta being the last command
    notesNoLongerInProgress=[]
    for note in notesInProgress:
        rec=notesInProgress[note]
        if (rec.lastTimestamp < (tst-chatterLimit)) or (cmd=="Meta"):
            if rec.originalCommand == rec.lastCommand:
                addToOutput(rec.originalLine)
            notesNoLongerInProgress.append(note)
    for note in notesNoLongerInProgress:
        del notesInProgress[note]
        
    # If the command is Meta, move it to output
    if cmd=="Meta":
        addToOutput(cline)
        continue
    
    # at this point the command is On or Off 
    # only notes with the last command under the chatter limit ago are in notesInProgress
    note=noteName(cline)
    if not (note in notesInProgress):
        noteIP=types.SimpleNamespace(originalLine=cline)
        noteIP.originalCommand=cmd 
        noteIP.lastCommand=cmd 
        noteIP.lastTimestamp=tst
        notesInProgress[note]=noteIP
    else:
        notesInProgress[note].lastCommand=cmd
        notesInProgress[note].lastTimestamp=tst
 
if notesInProgress!={}:
     print("notesInProgress not empty - last command was not Meta?")
     print(notesInProgress)
     
open(sys.argv[2],"w").writelines(outputLines)
