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
grid = [ [ int(c) for c in line ] for line in lines ]

min_row, max_row = 0, len ( grid ) - 1
min_col, max_col = 0, len ( grid[0] ) - 1

def adjacent_coordinates (x, y):
    # without diagonal ones
    candidates = [ (x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y)]

    return [ (a, b) for a, b in candidates if a >= min_row and a <= max_row and \
                                              b >= min_col and b <= max_col ]

def is_low_point ( x, y ):
    return all ( grid[x][y] < grid[a][b] for (a, b) in adjacent_coordinates ( x, y ) )

def get_baisin_size ( x, y ):
    # set yourself as visited
    visited . add ( (x,y) )

    return 1 + sum ( [ get_baisin_size (a, b) for (a, b) in adjacent_coordinates (x, y) if \
                                       (a, b) not in visited and grid[a][b] != 9 ] )

low_points = [ (x, y) for x in range ( len (grid) ) for y in range ( len (grid[x])) if is_low_point ( x, y) ]

visited = set ( low_points )

sizes = sorted ( [ get_baisin_size (x, y) for (x, y) in low_points] )

prod = 1
for i in range ( 3 ):
    prod *= sizes [ len ( sizes ) - 1 - i ]

print ( prod )