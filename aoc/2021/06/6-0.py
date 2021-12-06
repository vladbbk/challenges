#!/usr/bin/env python3
import os, sys

if len ( sys.argv ) != 2:
    print ( "you didn't specify the input file!")
    exit(1)

if not os.path.exists ( sys.argv[1] ) or not os.path.isfile ( sys.argv[1]):
    print ( "input file does not exists or isn't a file!" )
    exit(1)


with open ( sys.argv[1], "r") as f:
    lines = [ line . strip () for line in f.readlines() ]

# ------------------------------------------------------------------------
DAYS = 80
fishes = [ int(x) for x in lines[0].split(',')]

# naive approach, O(days*len(fishes))
print ( f"Initial state: {fishes}")
for day in range ( DAYS ):
    for i in range ( len (fishes) ):
        if fishes[i] == 0:
            fishes[i] = 6
            fishes.append ( 8 )
        else:
            fishes[i] -= 1
    print (f"After {day+1} day: {len(fishes)}")

print (f"After {DAYS} there are {len(fishes)} fishes")
