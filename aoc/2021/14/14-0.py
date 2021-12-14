#!/usr/bin/env python3
import os, sys
from typing import DefaultDict

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
from collections import Counter

template = lines[0]
rules = { x: y for x, y in ( line.split ( " -> ") for line in lines[2:] ) }

steps = 4

# first attempt => manual string creation
result = template
# ========================================================================
for step in range ( steps ):
    new_string = ""
    for char_pos in range ( len ( result ) - 1 ):
        pattern = result[char_pos] + result[char_pos+1]
        if pattern in rules:
            # if it is the absolute first char, keep it
            # otherwise no, because they overlap
            if char_pos == 0:
                new_string += result[char_pos]

            new_string += rules [ pattern ] + result [ char_pos + 1 ]

    result = new_string
# ========================================================================

counter = Counter ( result ) . most_common ()
most_common, least_common = counter[0], counter[-1]
diff = most_common[1] - least_common[1]

print ( f"{most_common[0]} - {least_common[0]} == {diff}" )
