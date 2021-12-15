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
# the problem can be reformulated to find shortest path 
# let's use Dijkstra for this one?
# https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm
import math
from queue import PriorityQueue

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

print ( f"lowest risk factor: {distances[_to]}")
