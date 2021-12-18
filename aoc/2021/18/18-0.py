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
import json
import math

class Snailfish:
    def __init__(self, str) -> None:
        self.number = json.loads ( str )
        self.depth = self.compute_depth ( self.number )

        self.explosion_occured = False
        self.split_occured     = False

        self.left_propagation  = None
        self.right_propagation = None

        self.visited = []

    def __repr__(self) -> str:
        s = str ( self.number ) . replace ( ' ', '' )
        return f"Snailfish number: {s} ({self.depth})"

    def __add__ (self, __o):
        self.number = [ self.number, __o.number ]
        self.depth = max ( self.depth, __o.depth) + 1

        # print ( f" depth after addition: {self.depth}")

        self.loop ()

        return self

    def loop ( self ):
        # only to ensure that the first iteration will be executed
        self.split_occured = True

        while self.split_occured:
            # recompute the depth
            self.depth = self.compute_depth ( self.number )

            # reset the `split occured` flag
            self.split_occured = False

            # make sure the depth is < 5
            # print ( f" before keep exploding, depth: {self.depth}")
            self.keep_exploding ()

            # now attempt to split
            self.number = self.split ( self.number )

    def keep_exploding ( self ):
        # keep exploding until depth < 5
        while self.depth > 4:
            # reset the visited lists
            self.visited = []
            #print ( f" - depth > 5, we should reduce: {self}" )
            self.number = self.explode ( self.number )

            self.depth = self.compute_depth ( self.number )


            # reset the explosion flag and propagation numbers
            # (if you didn't encounter any integers on way back, therefore they weren't erased)
            self.explosion_occured = False
            self.left_propagation = None
            self.right_propagation = None

            #print ( f" - exploded number: {self}")
            #print ( f"---------------------------------------------------")

        # after all possible explosions, 

    def explode (self, _list, depth = 0, spaces = ''):
        left_part, right_part = _list[0], _list[1]

        if isinstance (left_part, int ) and isinstance ( right_part, int ) and depth == 4:
            # print ( f"{spaces} - reached the end of two integers: [{left_part},{right_part}], returning ..." )
            # the explosion has to occur here -- if it hasn't already!

            if not self.explosion_occured:
                # print ( f"{spaces}   - explosion has not yet occured, exploding ... ")
                self.explosion_occured = True

                self.left_propagation = left_part
                self.right_propagation = right_part

                # add the new one to the visited
                self.visited . append ( 0 )

                return 0

        new_left_part = left_part if isinstance ( left_part, int ) else self.explode(left_part, depth + 1, spaces + ' ')

        # you have completed the both parts -- did an explosion occur?
        if self.explosion_occured:
            # print ( f" -- EXPLOSION OCCURED IN CHILD, exiting ... {depth}: [{left_part},{right_part}]" )
            if self.left_propagation:
                # if it is a simple integer, just overwrite it
                if isinstance ( left_part, int ):
                    left_part += self.left_propagation
                    self.left_propagation = None
                
                # but if it is a list AND it is not in visited,
                # insert to the nearest right position

            if self.right_propagation:
                if isinstance ( right_part, int ):
                    right_part += self.right_propagation
                    self.right_propagation = None
                else:
                    right_part = self.rec_propage_right ( right_part )
                    #right_part[0] += self.right_propagation
                    #self.right_propagation = None
                    #print ( f" --- the right part is not an integer: {right_part}, {self.right_propagation}, {self.left_propagation}")

            new_list = [new_left_part, right_part]
            return new_list

        new_right_part = right_part if isinstance ( right_part, int ) else self.explode(right_part, depth + 1, spaces + ' ')

        # you have completed the both parts -- did an explosion occur?
        if self.explosion_occured:
            # print ( f" -- EXPLOSION OCCURED IN CHILD, exiting ... {depth}: [{left_part},{right_part}]" )

            if self.left_propagation:
                if isinstance ( left_part, int ):
                    left_part += self.left_propagation
                    self.left_propagation = None
                else:
                    # assume that it is only a one-pair
                    left_part = self.rec_propage_left ( left_part )
                    #left_part[1] += self.left_propagation
                    #self.left_propagation = None
                    #print ( f" --- the left part is not an integer: {right_part}")

            if self.right_propagation:
                if isinstance ( right_part, int ):
                    right_part += self.right_propagation
                    self.right_propagation = None

            new_list = [left_part, new_right_part]

            return new_list

        # --------------------------------------------

        return [new_left_part, new_right_part ]

    def rec_propage_right (self, _list):
        left, right = _list[0], _list[1]

        if isinstance ( left, int ):
            new_list = [left + self.right_propagation, right ]
            self.right_propagation = None
            return new_list

        # else -> left is a list
        return [ self.rec_propage_right ( left ), right]

    def rec_propage_left (self, _list):
        left, right = _list[0], _list[1]

        if isinstance ( right, int ):
            new_list = [left, right + self.left_propagation ]
            self.left_propagation = None
            return new_list

        # else -> left is a list
        return [ left, self.rec_propage_left ( right ) ]


    def split (self, _list, spaces = ''):

        if isinstance ( _list, int ):
            new_pair = _list
            if _list >= 10 and not self.split_occured:
                new_pair = [ math.floor ( _list / 2 ), math.ceil ( _list/2 ) ]
                self.split_occured = True

            return new_pair

        # if it is not an integer
        return [ self . split (_list[0]), self . split (_list[1]) ]

    def compute_depth ( self, _list ):
        if not isinstance (_list, list):
            return 0

        return 1 + max ( self.compute_depth ( item ) for item in _list )

    def compute_maginutude ( self ):
        return self.rec_magnitude ( self.number )

    def rec_magnitude ( self, _list ):
        if isinstance ( _list[0], int ):
            left = 3 * _list[0]
        else:
            left = 3 * self.rec_magnitude ( _list[0] )

        if isinstance ( _list[1], int ):
            right = 2 * _list[1]
        else:
            right = 2 * self.rec_magnitude ( _list[1] )

        return left + right


snail_numbers = [ Snailfish ( line ) for line in lines ]
first_snail = snail_numbers[0]



for i in range ( len ( snail_numbers ) - 1 ):
    first_snail = first_snail + snail_numbers[i + 1]
    print ( f" - after addition: {first_snail}")

print ( f"final sum is: {first_snail}")

print ( first_snail.compute_maginutude() )
