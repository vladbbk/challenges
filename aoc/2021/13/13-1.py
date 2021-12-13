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
    lines = sys.argv[1] . split ( '\n' )[:-1]

lines = [ line . strip () for line in lines ]
# ------------------------------------------------------------------------
class TuppleWrapper:
    def __init__(self, line ) -> None:
        x, y = line . split ( ',' )
        self.coords = {
            0: int ( x ),
            1: int ( y )
        }

    def __getitem__ ( self, key ):
        return self.coords [ key ]

    def __hash__(self) -> int:
        return hash ( tuple (self.coords.keys()) )

    def __eq__(self, __o: object) -> bool:
        return self[0] == __o[0] and self[1] == __o[1]

    def __setitem__ ( self, key, val ):
        self.coords [ key ] = val
# ------------------------------------------------------------------------
axes = [ 'x', 'y' ]

dots = [ TuppleWrapper ( line ) for line in lines if ',' in line ]
folds = [ [line[11], line.split ( '=')[1]] for line in lines if '=' in line ]

# keep folds as tuple of (<index of axis>, <integer point of fold>)
folds = [ (axes . index (axis), int(pos)) for axis, pos in folds ]

print ( f"total points: {len(dots)}")

for axis, point in folds:
    dots_below = set ( filter ( lambda p: p[axis] > point, dots ) )
    dots_above = set ( filter ( lambda p: p[axis] < point, dots ) )

    # update the positions of the dots below
    for dot in dots_below:
        dot[axis] = point - ( dot[axis] - point )
    
    dots = dots_above.union ( dots_below )

X_MAX = max ( [ wrapper[0] for wrapper in dots ] )
Y_MAX = max ( [ wrapper[0] for wrapper in dots ] )

for y in range ( Y_MAX + 1 ):
    for x in range ( X_MAX + 1 ):
        if TuppleWrapper( f"{x},{y}" ) in dots:
            print ( "x", end='')
        else:
            print ( ' ', end='')

    print ()
