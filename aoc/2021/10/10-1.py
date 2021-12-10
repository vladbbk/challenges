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
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4
}

def incomplete ( string ):
    queue = []
    for c in string:
        if c in opens:
            queue . append ( closes [ opens.index (c) ] )

        if c in closes:
            # it must match the last character in queue
            if not queue or c != queue [ len ( queue ) - 1 ]:
                return None

            # else remove from the queue
            queue . pop ()

    # -> incomplete
    if queue:
        score = 0
        queue . reverse ()
        for c in queue:
            score *= 5
            score += scoring [ c ]
        
        return score
    return None

scores = [ incomplete ( line ) for line in lines ]
scores = sorted ( filter ( None, scores ) )

print ( f"middle of incomplete: {scores [ len ( scores ) // 2]}")