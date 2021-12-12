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
from copy import deepcopy
graph = {}

# create the graph
for line in lines:
    _from, _to = line . split ( '-' )
    
    if _from not in graph:
        graph [ _from ] = []

    if _to not in graph:
        graph [ _to ] = []

    graph [ _from ] . append ( _to )
    graph [ _to ] . append ( _from )

# adjusted dfs
def dfs_rec ( cave, visited, small_cave ):
    if cave == "end":
        return 1

    copy_small_cave = small_cave
        
    if cave.islower() and cave in visited:
        if small_cave or cave == "start":
            return 0

        copy_small_cave = cave

    
    copy = deepcopy ( visited )
    copy . add ( cave )

    return sum ( [ dfs_rec ( c, copy, copy_small_cave ) for c in graph [ cave ] ] )

paths = dfs_rec ( "start", set (), None )
print ( f"#paths: {paths}")