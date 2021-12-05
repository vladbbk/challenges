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

def overlaps ( x, y):
    grid [ x ] [ y ] += 1

    if grid [ x ] [ y ] > 1:
        overlapping . add ( (x,y) )

for line in lines:
    a, b = line . split ( '->' )
    x1, y1 = [ int ( c ) for c in a . split ( ',' ) ]
    x2, y2 = [ int ( c ) for c in b . split ( ',' ) ]

    left_point, right_point = ((x1,y1),(x2,y2)) if x1 < x2 else ((x2,y2),(x1,y1))

    if x1 == x2 or y1 == y2:
        axis = [x1,x2] if y1 == y2 else [y1,y2]
        start, end = min ( axis), max ( axis )

        for i in range (end - start + 1 ):
            if x1 == x2:
                overlaps ( x1, start + i )
            else:
                overlaps ( start + i, y1 )

    else:
        direction = 1 if left_point[1] < right_point[1] else -1

        for i in range ( right_point[0] - left_point[0] + 1):
            overlaps ( left_point[0] + i, left_point[1] + direction*i )


print ( f"overlapping points: {len ( overlapping )}")