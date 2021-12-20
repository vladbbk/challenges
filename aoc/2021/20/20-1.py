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
# light pixels: '#', 1
# dark pixels:  '.', 0

decoding = {}
for i, pixel in enumerate ( lines[0]):
    key = "". join ( [ '.' if bit == '0' else '#' for bit in format (i, '#011b')[2:] ] )
    decoding [ key ] = pixel

def generate_bigger_grid ( original_grid):
    # character
    # create grid with one more layer from both sides
    columns_amount = len ( original_grid[0] ) + 2
    grid = [ [ None ] * columns_amount ]

    for line in original_grid:
        grid . append ( [None ] + list ( line ) + [ None] )

    # append one more column
    grid . append (  [None] * columns_amount )

    return grid

def print_grid ( grid ):
    for line in grid:
        print ( "".join ( [ char if char else ' ' for char in line ] ) )


infinity_char = '.'

# grid, dummy1 = generate_bigger_grid ( lines[1:], '.' )
grid = [ [char for char in line ] for line in lines[1:]]
steps = 50

for step in range ( steps ):
    # generate new grid with +1 dimension
    new_grid = generate_bigger_grid ( grid )

    # now we need to adjust every single cell of this grid
    for i in range ( len ( new_grid ) ):
        for j in range ( len ( new_grid[i] ) ):

            # now we have to generate the key
            key = ""
            for x in [ -1, 0, 1]:
                for y in [ -1, 0, 1]:

                    # if we are out of bounds, then the character
                    # representing infinity pixel should be added
                    if (i + x) not in range ( 1, len ( new_grid ) - 1 ) or \
                        (j + y) not in range ( 1, len ( new_grid[i+x]) - 1):
                        key += infinity_char
                    else:
                        key += grid [ i + x - 1] [ j + y - 1 ]
            new_grid [ i ] [ j ] = decoding [ key ]
    grid = new_grid
    infinity_char = decoding [ infinity_char*9 ]

ans = sum ( [ row.count ( '#' ) for row in grid ]  )
print ( f"decoding size: {len (decoding)}, ans: {ans}")
