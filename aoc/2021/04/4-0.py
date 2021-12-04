#!/usr/bin/env python3
import os
import sys

if len(sys.argv) != 2:
    print("you didn't specify the input file!")
    exit(1)

if not os.path.exists(sys.argv[1]) or not os.path.isfile(sys.argv[1]):
    print("input file does not exists or isn't a file!")
    exit(1)


with open(sys.argv[1], "r") as f:
    lines = [line . strip() for line in f.readlines()]

# ------------------------------------------------------------------------


class BingoBoard:
    def __init__(self):
        self.rows = [[0]*5 for i in range(5)]
        self.cols = [[0]*5 for i in range(5)]

    def draw ( self, number ):
        winner = False
        for i in range ( 5):
            if number in self.cols[i]:
                self.cols[i] . remove ( number )
            
            if number in self.rows[i]:
                self.rows[i] . remove ( number )

            if not self.rows[i] or not self.cols[i]:
                winner = True

        if winner:
            # we should get all unique remaining numbers
            flat_rows = [num for row in self.rows for num in row ]
            flat_cols = [num for col in self.cols for num in col ]

            uniq = set ( flat_rows + flat_cols )
            res = number * sum ( uniq )

            print ( "WE HAVE A WINNER! WE SHOULD STOP NOW!")
            print ( uniq )
            print ( f"called number: {number}, sum: {sum(uniq)}, result: {res}")
            exit ( 1 )


drawn = [int(x) for x in lines.pop(0) . split(',')]

links = {}

for i in range(len(lines)):
    if lines[i] == "":

        board = BingoBoard()

        for j in range(5):
            numbers = [int(x) for x in lines[i+j+1] . split()]

            # input the created number into both columns and rows
            # row index ==> j
            # column index to be created

            #for k in range ( len ( numbers ) ):
            for idx, num in enumerate ( numbers ):
                board.rows[j][idx] = num
                board.cols[idx][j] = num

                # add link to this object
                if num not in links:
                    links [ num ] = [ board ]
                    continue
                    
                # and now check if board is already linked
                if board not in links [ num ]:
                    links [ num ] . append ( board )

for num in drawn:
    print ( f"trying number: {num}")
    if num not in links:
        print ( " --> number not present in any board, skipping ..." )
        continue


    for board in links[num]:
        board . draw ( num )
        links[num] . remove ( board )