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
    lines = sys.argv[1] . split ( '\n')

lines = [ line . strip () for line in lines ]
# ------------------------------------------------------------------------
WINNING_SCORE = 1000
BOARD_SIZE = 10
DETERMINISTIC_DICE_SIZE = 100

# indexes
POS = 0
SCORE = 1

A = 0
B = 1

# we have this weird indexing for easy determination of player on turn
players = [
    [int (lines[0] . split ( "starting position: " ) [1]), 0], # player A
    [int (lines[1] . split ( "starting position: " ) [1]), 0]  # player B
]

def next ( start, steps, modulo ) -> int:
    return (( start + steps - 1 ) % modulo ) + 1

rolled = 0
total_rolled = 0
ON_TURN = A

print ( f"A start: {players[A][POS]}, B start: {players[B][POS]}")

while players[A][SCORE] < WINNING_SCORE and players[B][SCORE] < WINNING_SCORE:
    steps = sum ( next ( rolled, i, DETERMINISTIC_DICE_SIZE ) for i in range ( 1, 4 ) )
    rolled = next ( rolled, 3, DETERMINISTIC_DICE_SIZE )

    players[ON_TURN][POS] = next ( players[ON_TURN][POS], steps, BOARD_SIZE )
    players[ON_TURN][SCORE] += players[ON_TURN][POS]
    
    total_rolled += 3
    ON_TURN = ( ON_TURN + 1 ) % 2

# if the while loop has stopped, the player NOT on turn has won
answer = total_rolled * players [ ON_TURN ] [ SCORE ]
print ( f" - dice rolled a total of {total_rolled} times " )
print ( f" - losing player's score: {players[ON_TURN][SCORE]}")
print ( f" - answer: {answer}")
# 518418 < ANS