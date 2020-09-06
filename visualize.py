#!/usr/bin/python3

import types
import sys

interval=50
channel_sizes={1:4,2:10,3:5,4:5}
max_digits_in_ms=8
#max_digits_in_shortened=5

def time_stamp(line):
    spl=line.split()
    try:
        return int(spl[0])
    except ValueError:
        return 0

def note_and_channel(line):
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
    return nt,ch
    
def command_name(line):
    spl=line.split()
    try:
        return spl[1]
    except IndexError:
        return ""

if len(sys.argv)<2 or len(sys.argv)>3:
    print("Usage: "+sys.argv[0]+" infile [outfile]")
    exit(1)

infile=sys.argv[1]
input_lines=open(infile).readlines()

if len(sys.argv)==3:
    outfile=sys.argv[2]
elif infile.find(".v")>0:
    outfile=infile.replace(".v",".vis",1)
else:
    outfile=infile+".vis"

next_line_time=0

# Output channel names and initialize note state
note_states={}
notes_turned_off={} 
    # track notes turned off separately, so if one is turned off and back on we know it
first_line=" "*max_digits_in_ms+"|"
for ch in channel_sizes:
    note_states[ch]={}
    notes_turned_off[ch]=set()
    # the next line works right only if all channels have single-digit numbers
    first_line+="Ch "+str(ch)+" "*4*(channel_sizes[ch]-1)+"|"
output_lines=[first_line+"\n"]

for cline in input_lines:
    tst=time_stamp(cline)
    cmd=command_name(cline)
    
    if cmd in ["On","Off"]: # only note on and off commands are processed
    
        if next_line_time==0: # this happens only in the very first note command
            next_line_time=interval*((tst//interval)+1)
            
        # output all lines that were not yet output but are before current time
        while next_line_time<tst:
            new_line=str(next_line_time).rjust(max_digits_in_ms)+"|"
            for ch in channel_sizes:
                for n in range(channel_sizes[ch]):
                    if n in note_states[ch]:
                        new_note=note_states[ch][n]
                        if new_note in notes_turned_off[ch]:
                            new_note+="/"
                        new_line+=new_note.ljust(4)
                    else:
                        new_line+="    "
                new_line+="|"
                notes_turned_off[ch]=set()
            output_lines.append(new_line+"\n")
            next_line_time+=interval
        
        nt,sch=note_and_channel(cline)
        ch=int(sch)
        
        if not (ch in note_states):
            print(tst,"ERROR: Unknown channel:",ch)
            continue

        if cmd=="On":
            if nt in note_states[ch].values():
                print(tst,"WARNING: On for note already on:",nt,"on channel:",ch)
                continue
            # find a position for new note in states
            i=0
            while i in note_states[ch]:
                i+=1
            if i>=channel_sizes[ch]:
                print(tst,"ERROR: Too many notes ON on channel:",ch)
                continue
            note_states[ch][i]=nt
        
        if cmd=="Off":
            if not (nt in note_states[ch].values()):
                print(tst,"WARNING: Off for note already off:",nt,"on channel:",ch)
                continue
            # find and remove the note
            notepos=65535
            for i in note_states[ch]:
                if note_states[ch][i]==nt:
                    notepos=i
            if notepos==65535:
                print(tst,"ERROR: note not found",nt,"on channel:",ch,"- this should never happen")
                continue
                
            del note_states[ch][notepos]
            notes_turned_off[ch].add(nt)

if len(output_lines)<3:
    print("ERROR: no meaningful result")
    exit(1)

            
# shorten the output
shortened_output=[]
counter=0
start_time=""
for i in range(len(output_lines)):
    same_as_next=False
    try:
        s2=output_lines[i+1][max_digits_in_ms:]
        s1=output_lines[i][max_digits_in_ms:]
        same_as_next=(s1==s2)
    except IndexError: pass
    if same_as_next:
        counter+=1
        if counter==1:
            start_time=output_lines[i][:max_digits_in_ms]
    else:
        prefix=" "*(max_digits_in_ms+1)
        if counter>0:
            prefix=start_time+"-"
        counter=0
        shortened_output.append(prefix+output_lines[i])

open(outfile,"w").writelines(shortened_output)
    