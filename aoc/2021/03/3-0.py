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


# O(len(num))
def inverse ( num ):
    res = ""
    for c in num:
        res += "0" if c == "1" else "1"
    
    return res



# O( len(lines) * len ( num ))
occurences_of_one = [0] * len ( lines[0] )
half = len ( lines ) // 2

for i in range ( len ( lines ) - 1 ):
    for c in range ( len ( lines[i]) - 1 ):
        if lines[i][c] == "1":
            occurences_of_one[c] += 1

print ( f"occurnces of ones: {occurences_of_one}, half: {half}")


# O(len(num))
# construct the string
binary = "". join ( [ "1" if oc >= half else "0" for oc in occurences_of_one] )
inv = inverse ( binary )

int_binary = int ( binary, 2)
int_inv = int ( inv, 2 )

print ( f"binary: {binary}, inverse: {inv}")
print ( f"in int representation -> binary: {int_binary}, inverse: {int_inv}")

print ( f"multiplication: {int_binary} * {int_inv} = {int_binary*int_inv}")
