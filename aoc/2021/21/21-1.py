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
from itertools import product
from collections import Counter
from copy import deepcopy
from functools import cache

WINNING_SCORE = 21
BOARD_SIZE = 10

# we have this weird indexing for easy determination of player on turn
A_pos = int ( lines[0] . split ( "starting position: " ) [1] )
B_pos = int ( lines[1] . split ( "starting position: " ) [1] )

def next ( start, steps, modulo ) -> int:
    return (( start + steps - 1 ) % modulo ) + 1

permutations = product ( [1,2,3], [1,2,3], [1,2,3] )
dirac = Counter ( [ sum ( permutation ) for permutation in permutations ] )

@cache
def recursion ( player_pos, player_score, waiting_pos, waiting_score ):
    if player_score >= WINNING_SCORE:
        return 1, 0

    if waiting_score >= WINNING_SCORE:
        return 0, 1


    # future result
    player_wins = 0
    other_wins = 0

    # no player won, therefore player on turn is playing
    # for every possible combination
    for rolled, times in dirac.items ():

        new_pos = next ( player_pos, rolled, BOARD_SIZE )
        new_score = new_pos + player_score

        _waiting, _playing = recursion ( waiting_pos, waiting_score, new_pos, new_score )

        other_wins += times * _waiting
        player_wins += times * _playing

    return player_wins, other_wins


total_results = recursion ( A_pos, 0, B_pos, 0 )
print ( max ( total_results ) )