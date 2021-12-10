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
opens  = [ '(', '[', '{', '<' ]
closes = [ ')', ']', '}', '>' ]

scoring = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137
}

def check ( string ) -> int:
    queue = []
    for c in string:
        if c in opens:
            queue . append ( closes [ opens.index (c) ] )

        if c in closes:
            # it must match the last character in queue
            if not queue or c != queue [ len ( queue ) - 1 ]:
                return scoring [ c ]

            # else remove from the queue
            queue . pop ()

    # print ( f"OK:        {string}")
    return 0

score = sum ( [ check ( line ) for line in lines ])

print ( f"achieved score: {score}")