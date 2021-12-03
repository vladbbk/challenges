#!/usr/bin/env python3
import sys

if len ( sys.argv ) != 2:
    print ( "you didn't specify the file!")
    exit(1)


with open ( sys.argv[1] + ".txt", "r") as f:
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