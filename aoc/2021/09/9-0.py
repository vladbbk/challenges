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
low_points = []
grid = [ [ int(c) for c in line ] for line in lines ]

min_row, max_row = 0, len ( grid ) - 1
min_col, max_col = 0, len ( grid[0] ) - 1

def adjacent_coords (x, y):
    candidates = [ (x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y)]

    return [ (a, b) for a, b in candidates if a >= min_row and a <= max_row and \
                                              b >= min_col and b <= max_col ]

def is_low_point ( x, y, adjacent_points ):
    return all ( grid[x][y] < grid[a][b] for (a, b) in adjacent_points)

for row in range ( len ( grid ) ):
    for col in range ( len ( grid [ row ] ) ):
        if is_low_point ( row, col, adjacent_coords ( row, col ) ):
            low_points . append ( grid [row][col] )

print ( sum ( [ point + 1 for point in low_points ] ) )
