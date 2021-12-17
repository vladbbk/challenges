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
    lines = sys.argv[1] . split ( '\n' )

lines = [ line . strip () for line in lines ]
# ------------------------------------------------------------------------
import functools
from itertools import product

# get the grid of the target, represented in two tuples:
x, y = lines[0][13:] . split ( ", " )
x_min, x_max = [ int ( coord ) for coord  in x[2:] . split ( ".." ) ]
y_min, y_max = [ int ( coord ) for coord  in y[2:] . split ( ".." ) ]

def point_in_target ( point ):
    return  x_min <= point[0] <= x_max and y_min <= point[1] <= y_max

def overshot_target ( point ):
    return point[0] > x_max or point[1] < y_min

def next_point ( point, velocity_vector ):
    # generate the new point
    new_point = point[0] + velocity_vector[0], point[1] + velocity_vector[1]

    # gravity -> decrease <y> of velocity vector by one
    y_acceleration = velocity_vector[1] - 1

    # if <x> field of velocity vector does not equal zero, 
    # increase/decrease <x> based on direction
    x_acceleration = velocity_vector[0]

    if x_acceleration != 0:
        x_acceleration += 1 if velocity_vector[0] < 0 else -1

    return new_point, (x_acceleration, y_acceleration)

def try_vector ( vector ):
    global absolute_y_max
    velocity = vector
    point = (0, 0) 

    while not overshot_target ( point ):
        point, velocity = next_point ( point, velocity )

        if point_in_target ( point ):
            absolute_y_max = max ( absolute_y_max, stops_in(vector[1]))
            break

@functools.cache
def stops_in ( x ):
    if x == 0 or x == 1:
        return x

    return x + stops_in ( x-1 )

possible_x = [ x for x in range ( x_min ) if x_min <= stops_in ( x ) <= x_max ]
possible_y = range ( (-1)*y_max, (-1)*y_min )

absolute_y_max = 0

for vector in product ( possible_x, possible_y ):
    try_vector ( vector )

print ( f"The highest position over <y> axis: {absolute_y_max}")
