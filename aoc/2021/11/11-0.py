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
import itertools
grid = { (x,y): int (lines[x][y]) for x in range ( len ( lines ) )  \
                                  for y in range ( len ( lines[x] ) ) }
steps = 100
flashes = 0

def get_adjacent_coords ( tuple ):
    candidates = [ (tuple[0] + i, tuple[1] + j) for (i, j) in itertools.product ( [-1, 0, 1], repeat=2 )]

    return filter ( lambda t: 0 <= t[0] < 10 and 0 <= t[1] < 10, candidates )

for step in range ( steps ):
    flashed = set ()
    increases = { octopus: 1 for octopus in grid . keys () }

    all_increased = False
    while not all_increased:
        all_increased = True

        for octopus in increases:
            if increases [ octopus ] != 0 and octopus not in flashed:
                if increases [ octopus ] + grid [ octopus ] > 9:
                    # 'flash' octopus
                    flashed . add ( octopus )
                    grid [ octopus ] = 0

                    # for every neighbor (which hasn't already flashed)
                    # increase the energy level addition and reset the loop
                    for neighbor in get_adjacent_coords ( octopus ):
                        if neighbor not in flashed:
                            increases [ neighbor ] += 1
                            all_increased = False
                else:
                    grid [ octopus ] += increases [ octopus ]
                    increases [ octopus ] = 0

    flashes += len ( flashed )

print ( f"total flashes after {steps} steps: {flashes}")