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
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4
}

def get_line_score ( string ) -> int:
    score = 0
    expected = []

    for char in string:
        if char in openings:
            expected . append ( closings [ openings.index (char) ] )

        if char in closings:
            # it must match the last character in expected
            if not expected or char != expected[-1]:
                return score

            # else remove from the expected
            expected . pop ()

    for char in reversed ( expected ):
        score = score*5 + scoring [ char ]

    return score

scores = [ get_line_score ( line ) for line in lines ]
scores = sorted ( filter ( lambda n: n != 0, scores ) )

print ( f"middle of incomplete: {scores [ len ( scores ) // 2]}")