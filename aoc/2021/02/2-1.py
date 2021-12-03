#!/usr/bin/env python3
import os, sys

if len ( sys.argv ) != 2:
    print ( "you didn't specify the input file!")
    exit(1)

filename = sys.argv[1] + ".txt"

if not os.path.exists ( filename ) or not os.path.isfile ( filename):
    print ( "input file does not exists or isn't a file!" )
    exit(1)


with open ( filename, "r") as f:
    lines = [ line . strip () for line in f.readlines() ]

# ------------------------------------------------------------------------

horizontal = 0
vertical = 0
aim = 0


for line in lines:
    words = line . split ( ' ' )
    amount = int ( words[1])


    if words[0] == "forward":
        horizontal += amount
        vertical += aim * amount

    else:
        aim += -amount if words[0] == "up" else amount


print ( f"vertical: {vertical}, horizontal: {horizontal}, res: {vertical*horizontal}")