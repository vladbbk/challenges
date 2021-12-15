#!/usr/bin/env python3
import os, sys

if len ( sys.argv ) != 2:
    print ( f"usage: {sys.argv[0]} <input/input file>")
    exit(1)

if os.path.exists ( sys.argv[1] ) and os.path.isfile ( sys.argv[1]):
    # if a file exists with that input, read from the file
    with open ( sys.argv[1], "r" ) as f:
        lines = f . readlines ()
else:
    # otherwise treat input as lines
    lines = sys.argv[1] . split ()

lines = [ line . strip () for line in lines ]
# ------------------------------------------------------------------------
# as for path 2, can we continue using Dijkstra, but we have to update input
# this is messy, but I haven't had a lot of time for this and I actually
# didn't want to spend time on this

new_lines = []

def increment_grid ( grid ):
    # convert all lines to int 
    converted = [ [ int ( char ) for char in line ] for line in grid ]

    # increase them all 
    for i in range ( len ( converted ) ):
        for j in range ( len ( converted[i]) ):
            num = converted[i][j]

            converted[i][j] = (num + 1) if num != 9 else 1

    return [ "".join ([ str ( num ) for num in line ]) for line in converted ]

new_lines = []
current_grid = lines
for row in range ( 5 ):
    # create 'increment' of the last increment 
    next_increment = increment_grid ( current_grid )

    # create all increments
    increments = [ current_grid, next_increment ]
    for i in range ( 3 ):
        increments . append (increment_grid ( increments[-1] ) )
    
    for i in range ( len (current_grid) ):
        new_line = current_grid[i]
        
        for j in range ( 4 ):
            new_line += increments [ j + 1 ] [i]

        new_lines . append ( new_line )

    current_grid = next_increment

# replace old lines
lines = new_lines 
print ( "creation of new lines passed")
# ------------------------------------------------------------------------
import math
from queue import PriorityQueue
import time

graph = { (x,y): int (lines[x][y]) for x in range ( len ( lines ) )  \
                                   for y in range ( len ( lines[x] ) ) }

# grid is square
_min, _max = 0, len ( lines )


def get_adjacent_coords ( tuple ):
    # we _cannot_ move diagonally
    x, y = tuple
    candidates = [
        (x + 1, y),
        (x - 1, y),
        (x, y + 1),
        (x, y - 1)
        ]

    return list (filter ( lambda t: _min <= t[0] < _max and _min <= t[1] < _max, candidates))

_from, _to = (0,0), ( _max - 1, _max - 1 )

# initialization
distances = { vertex: math.inf for vertex in graph }
previous_verteces = { vertex: None for vertex in graph }

time_start = time.time()

def dijkstra ( start ):
    distances [ start ] = 0

    queue = [ start ]

    while queue:
        vertex = queue . pop ( 0 )

        for neighbor in get_adjacent_coords ( vertex ):
            alt = distances [ vertex ] + graph [ neighbor ]

            if alt < distances [ neighbor ]:
                distances [ neighbor ] = alt
                previous_verteces [ neighbor ] = vertex
                queue . append ( neighbor )


        queue = sorted ( list(set ( queue )), key=lambda v: distances[v] )

dijkstra ( _from ) 

print ( f"dijkstra has finished, took: {time.time()-time_start}")

print ( f"lowest risk factor: {distances[_to]}")
