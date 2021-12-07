#!/usr/bin/env python3
import os, sys
import math

if len ( sys.argv ) != 2:
    print ( "you didn't specify the input file!")
    exit(1)

if not os.path.exists ( sys.argv[1] ) or not os.path.isfile ( sys.argv[1]):
    print ( "input file does not exists or isn't a file!" )
    exit(1)


with open ( sys.argv[1], "r") as f:
    lines = [ line . strip () for line in f.readlines() ]

# ------------------------------------------------------------------------
crab_positions = [ int(c) for c in lines[0] . split (',') ]
fuel_positions = [0]*max(crab_positions)

# naive solution -> try each one
min = math.inf
for i in range ( len(crab_positions) ):
    total = sum ( [abs( i - crab_pos ) for crab_pos in crab_positions ])
    if total < min:
        min = total

print ( f"minimal sum of distances: {min}")
