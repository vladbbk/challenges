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
openings = [ '(', '[', '{', '<' ]
closings = [ ')', ']', '}', '>' ]

scoring = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137
}

def get_string_score ( string ) -> int:
    expected = []
    
    for char in string:
        if char in openings:
            expected . append ( closings [ openings.index (char) ] )

        if char in closings:
            # it must match the last character in expected
            if not expected or char != expected[-1]:
                return scoring [ char ]

            # else remove from the expected
            expected . pop ()

    return 0

score = sum ( [ get_string_score ( line ) for line in lines ])

print ( f"achieved score: {score}")