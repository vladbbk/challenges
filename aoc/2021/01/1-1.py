#!/usr/bin/env python3

with open ( "input.txt", "r") as f:
    numbers = [ int ( line . strip () ) for line in f.readlines() ]

# ------------------------------------------------------------------------

cnt = 0
last = None
for i in range ( len ( numbers ) - 1 - 1):
    num = sum ( [numbers[i], numbers[i+1], numbers[i+2] ] )

    if not last:
        last = num
        print ( f"{last} - N/A no previous measurement")
        continue

    if num > last:
        print ( f"{num} - [INCREASED]")
        cnt += 1

    else:
        print ( f"{num} - [decreased]")

    last = num

print ( f"----------------\ntotal increased: {cnt}")

# linear time
