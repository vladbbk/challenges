#!/usr/bin/env python3
import os, sys
from posix import X_OK

if len ( sys.argv ) != 2:
    print ( "you didn't specify the input file!")
    exit(1)

if not os.path.exists ( sys.argv[1] ) or not os.path.isfile ( sys.argv[1]):
    print ( "input file does not exists or isn't a file!" )
    exit(1)


with open ( sys.argv[1], "r") as f:
    lines = [ line . strip () for line in f.readlines() ]

# ------------------------------------------------------------------------
total = 0
for entry in lines:
    patterns, digits = [x.split() for x in entry . split ( ' | ')]
    total += len ( [ d for d in digits if len ( d ) in [ 2, 3, 4, 7 ] ] )

print ( f"total: {total}")