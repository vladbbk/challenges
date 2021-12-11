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
import copy
grid = { (x,y): int (lines[x][y]) for x in range ( len ( lines ) )  \
                                  for y in range ( len ( lines[x] ) ) }
steps = 0
flashes = 0

def get_adjacent_coords ( x, y ):
    candidates = [
        ( x - 1, y ),
        ( x + 1, y ),
        ( x, y - 1 ),
        ( x, y + 1 ),
        ( x + 1, y + 1 ),
        ( x - 1, y - 1 ),
        ( x + 1, y - 1 ),
        ( x - 1, y + 1 )
    ]

    return list ( filter ( lambda t: 0 <= t[0] < 10 and 0 <= t[1] < 10, candidates ) )

while True:
    flashed = set ()
    queue = { (x, y): 1 for x, y in grid . keys () }
    iteration = 0

    all_increased = False

    while not all_increased:
        all_increased = True

        for octopus in queue:
            increases = queue [ octopus ]

            if increases != 0:
                #print ( f"increasing {octopus} from: [{grid[octopus]}], with [{queue[octopus]}]")

                if octopus not in flashed:
                    if increases + grid [ octopus ] > 9:
                        flashed . add ( octopus )
                        grid [ octopus ] = 0
                        for adj in get_adjacent_coords ( octopus[0], octopus[1] ):
                            
                            # the number of increases in queue should be increased
                            # only if the adjacent octopus did not flash

                            # if the adjacent octopus has already been processed,
                            # it should be processed once again, cuz it didn't flash
                            if adj not in flashed:
                                queue [ adj ] += 1
                                all_increased = False
                                #print ( f"  - adj: {adj} should be increased: {queue[adj]}")
                    else:
                        grid [ octopus ] += increases
                        queue [ octopus ] = 0
            
        iteration += 1

    steps += 1
    flashed_in_step = len ( flashed )
    flashes += steps

    if flashed_in_step == 100:
        break
    


print ( f"100 octopuses flashed after steps {steps}")