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

def O2_criteria ( ones, zeroes ):
    if len ( ones ) > len ( zeroes ):
        return ones
    elif len ( ones ) < len ( zeroes ):
        return zeroes

    # if the result is same, return ones
    return ones


def CO2_criteria ( ones, zeroes ):
    if len ( ones ) > len ( zeroes ):
        return zeroes
    elif len ( ones ) < len ( zeroes ):
        return ones

    # if the result is same, return ones
    return zeroes

def filter ( array, criteria_func ):
    cyclic = 0
    num_length = len ( array[0] )
    while len ( array ) > 1:
        ones = [ num for num in array if num [ cyclic % num_length] == "1" ]
        zeroes = [ num for num in array if num [ cyclic % num_length] == "0" ]

        # now we should select the correct array based on the criteria
        array = criteria_func ( ones, zeroes )

        # increment cyclic and continue
        cyclic += 1
        array = criteria_func ( ones, zeroes )
    return int ( array[0], 2 )

O2 = filter ( lines, O2_criteria )
CO2 = filter ( lines, CO2_criteria )
LIFE_SUPPORT_RATING = O2 * CO2

print ( f"O2: {O2}, CO2: {CO2}, LIFE SUPPORT RATING: {LIFE_SUPPORT_RATING}")


