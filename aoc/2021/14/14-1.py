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
"""
DISCLAIMER: I was not able to solve this challenge.

I was able to get the final count of `combinations`,
but I didn't perceive that I can save the newly generated
character into global count, therefore I was looking into 
ways to preserve the order/determine the generated characters.

The challenge was 90% solved, I knew the direction, but wasn't 
able to drive it home.
""" 

template = lines[0]
rules = { x: y for x, y in ( line.split ( " -> ") for line in lines[2:] ) }

steps = 40

# occurences of each single character in the whole string
occurences = { char: 0 for char in rules.values () }
combination_occurences = { comb: 0 for comb in rules.keys() }

# fill the current combination occurences
for i in range ( len ( template ) - 1 ):
    combination_occurences [ template[i:i+2] ] += 1

# fill the resulting occurences of all characters
for char in template:
    occurences [ char ] += 1

for step in range ( steps ):
    # initialize count for each combination in the next step
    next_combination_occurences = { comb: 0 for comb in rules.keys() }

    # each combination will generate the character defined in rules * (count)
    for combination, count in combination_occurences . items ():
        generated_character = rules [combination]

        if generated_character not in occurences:
            occurences [ generated_character ] = 0

        occurences [ generated_character ] += count

        # and add two new combinations:
        left_char, right_char = combination[0], combination[1]

        next_combination_occurences [ left_char + generated_character ] += count
        next_combination_occurences [ generated_character + right_char ] += count

    # switch previous occurences with current one
    combination_occurences = next_combination_occurences

most_common = max ( occurences.values () )
least_common = min ( occurences.values () )

print ( f"{most_common} - {least_common} = {most_common-least_common}")
