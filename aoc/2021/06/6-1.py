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
import math

DAYS = 256
fishes = [ int(x) for x in lines[0].split(',')]

counter = {
        0: 0,
        1: 0,
        2: 0,
        3: 0,
        4: 0,
        5: 0,
        6: 0,
        7: 0,
        8: 0
    }

# compute the first counter 
for num in fishes:
    counter [ num ] += 1

# clever iterations -> as much as we can
counter_iterations = math.floor (DAYS / 7 )
print ( f"counter_iterations: {counter_iterations}")

print ( f"Initial state: {fishes}")
for day in range ( counter_iterations ):
    # after seven days, each number except [7,8]
    # produces the same amount of new <num>+2 numbers
    counter = {
        0: counter[0] + counter[7],
        1: counter[1] + counter[8],
        2: counter[2] + counter[0],
        3: counter[3] + counter[1],
        4: counter[4] + counter[2],
        5: counter[5] + counter[3],
        6: counter[6] + counter[4],
        7: counter[5],
        8: counter[6]
    }
    print (f"After {(day+1)*7} day: {sum(counter.values())}")

# for the remaining days (guaranteed <7), naive approach
for j in range ( DAYS - (counter_iterations*7)):
    counter = {
        0: counter[1],
        1: counter[2],
        2: counter[3],
        3: counter[4],
        4: counter[5],
        5: counter[6],
        6: counter[0] + counter[7],
        7: counter[8],
        8: counter[0],
    }
    print (f"After {(counter_iterations*7)+j+1} day: {sum(counter.values())}")

print (f"After {DAYS} there are {sum(counter.values())} fishes")