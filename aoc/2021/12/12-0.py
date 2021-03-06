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
from collections import defaultdict
graph = defaultdict ( list )

# create the graph
for line in lines:
    _from, _to = line . split ( '-' )

    graph [ _from ] . append ( _to )
    graph [ _to ] . append ( _from )

# adjusted dfs
def dfs_rec ( cave, visited ):
    if cave == "end":
        return 1

    if cave.islower() and cave in visited:
        return 0

    return sum ( [ dfs_rec ( c, visited.union ( {cave}) ) for c in graph [ cave ] ] )

paths = dfs_rec ( "start", set () )
print ( f"#paths: {paths}")
