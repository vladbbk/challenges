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
GRID_SIZE = 1000
grid = [ [0]*GRID_SIZE for i in range (GRID_SIZE) ]

overlapping = set()

for line in lines:
    a, b = line . split ( '->' )
    x1, y1 = [ int ( c ) for c in a . split ( ',' ) ]
    x2, y2 = [ int ( c ) for c in b . split ( ',' ) ]

    if x1 == x2:
        start, end  = min ( [y1, y2] ), max ( [y1,y2] )
        for i in range ( end - start + 1 ):

            grid [ x1 ] [ start + i ] += 1
            
            if grid [ x1 ] [ start + i ] > 1:
                overlapping.add ( (x1, start + i))

    if y1 == y2:
        start, end  = min ( [x1, x2] ), max ( [x1,x2] )
        for i in range ( end - start + 1 ):

            grid [ start + i ] [ y1 ] += 1

            if grid [ start + i ] [y1] > 1:
                overlapping.add( (start+i, y1) )

print ( len ( overlapping ))

