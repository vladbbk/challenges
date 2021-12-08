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
"""
acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf
   8                       7                 4          1

basic lengths :
    2 --> digit 1
    3 --> digit 7
    4 --> digit 4
    7 --> digit 8

I can definitely know which the top one is:
    - TOP HORIZONTAL: 7 - 1
    - BOT HORIZONTAL: 9 ( 4 + TOP_HORIZONTAL ) 

=======================================
  7:      8:      1:      4:
 aaaa    aaaa    ....    ....
.    c  b    c  .    c  b    c
.    c  b    c  .    c  b    c
 ....    dddd    ....    dddd
.    f  e    f  .    f  .    f
.    f  e    f  .    f  .    f
 ....    gggg    ....    ....

 =======================================

  0:      2:      3:     5:      6:      9:
 aaaa    aaaa    aaaa   aaaa    aaaa    aaaa
b    c  .    c  .    c b    .  b    .  b    c
b    c  .    c  .    c b    .  b    .  b    c
 ....    dddd    dddd   dddd    dddd    dddd
e    f  e    .  .    f .    f  e    f  .    f
e    f  e    .  .    f .    f  e    f  .    f
 gggg    gggg    gggg   gggg    gggg    gggg

=======================================

two things are definitely displayed

"""

def retrieve ( items, length ):
    ITEM = next ( it for it in items if len ( it ) == length)
    items . remove ( ITEM )
    return ITEM

def exclusive ( str ):
    res = ""
    occurences = [0] * 26
    for c in str:
        occurences [ ord ( c ) - 97 ] += 1

    for i in range ( len ( occurences ) ):
        if occurences[i] == 1:
            res += chr ( i + 97)

    return res

def unique ( str ):
    return "".join(set(str))

def contains_all_characters ( str, characters ):
    return all ( ( c in str ) for c in characters )

def get_decoder ( patterns ):
    # get the known ones
    ONE = retrieve ( patterns, 2 )
    FOUR = retrieve ( patterns, 4 )
    SEVEN = retrieve ( patterns, 3 )
    EIGHT = retrieve ( patterns, 7 )

    # determine the code for TOP HORIZONTAL
    TOP_HOR = exclusive ( ONE + SEVEN) 

    NINE = [ pt for pt in patterns if all ( ( c in pt) for c in unique ( SEVEN + FOUR ) ) ][0]
    patterns . remove ( NINE )

    BOT_HOR = exclusive ( SEVEN + FOUR + NINE )
    BOT_LEFT = exclusive ( EIGHT + NINE )

    TWO = [ pt for pt in patterns if BOT_LEFT in pt and len ( pt ) == 5 ][0]
    patterns . remove ( TWO )

    THREE = [ pt for pt in patterns if len ( pt ) == 5 \
        and contains_all_characters (unique (pt + BOT_LEFT), ONE) ][0]
    patterns . remove ( THREE )

    FIVE = [ pt for pt in patterns if len ( pt ) == 5 ][0]
    patterns . remove ( FIVE )

    SIX = [ pt for pt in patterns if contains_all_characters ( pt, FIVE ) ][0]
    patterns . remove ( SIX )

    ZERO = retrieve ( patterns, 6 )

    MIDDLE_HOR = exclusive ( EIGHT + ZERO )
    TOP_RIGHT = exclusive ( EIGHT + SIX )
    TOP_LEFT = exclusive ( EIGHT + ( SEVEN + MIDDLE_HOR + BOT_HOR + BOT_LEFT ) )
    BOT_RIGHT = exclusive ( EIGHT + (TWO + TOP_LEFT ) )

    return {
        "". join ( sorted ( [ TOP_HOR, BOT_HOR, TOP_LEFT, TOP_RIGHT, BOT_LEFT, BOT_RIGHT ] ) ): 0,
        "". join ( sorted ( [ TOP_RIGHT, BOT_RIGHT ]) ): 1,
        "". join ( sorted ( [ TOP_HOR, TOP_RIGHT, MIDDLE_HOR, BOT_LEFT, BOT_HOR ]) ): 2,
        "". join ( sorted ( [ TOP_HOR, TOP_RIGHT, MIDDLE_HOR, BOT_RIGHT, BOT_HOR ]) ): 3,
        "". join ( sorted ( [ TOP_LEFT, TOP_RIGHT, MIDDLE_HOR, BOT_RIGHT ]) ): 4,
        "". join ( sorted ( [ TOP_HOR, TOP_LEFT, MIDDLE_HOR, BOT_RIGHT, BOT_HOR ]) ): 5,
        "". join ( sorted ( [ TOP_HOR, MIDDLE_HOR, BOT_HOR, TOP_LEFT, BOT_LEFT, BOT_RIGHT ]) ): 6,
        "". join ( sorted ( [ TOP_HOR, TOP_RIGHT, BOT_RIGHT ]) ): 7,
        "". join ( sorted ( [ TOP_HOR, MIDDLE_HOR, BOT_HOR, BOT_RIGHT, BOT_LEFT, TOP_LEFT, TOP_RIGHT ]) ): 8,
        "". join ( sorted ( [ TOP_HOR, MIDDLE_HOR, BOT_HOR, BOT_RIGHT, TOP_LEFT, TOP_RIGHT ]) ): 9
    }

numbers = []
for entry in lines:
    patterns, digits = [x.split() for x in entry . split ( ' | ')]

    decoder = get_decoder ( patterns )
    digits = [ "". join ( sorted (c for c in dig) ) for dig in digits ]
    numbers . append ( int ( "".join ( [ str(decoder [ dig ] ) for dig in digits ] ) ) ) 

print ( sum ( numbers ) )