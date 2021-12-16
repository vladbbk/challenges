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
# CONSTANTS
VERSION_LENGTH = 3
TYPE_LENGH     = 3
LITERAL_CHUNK  = 5
BYTE           = 4

OPERATOR_MODE_LEN   = 1
OPERATOR_PACKET_NUM = 11
OPERATOR_BIT_LENGTH = 15

# input -- be careful, int is trimming leading zeroes
binary = "". join ( [ format (int ( hex_char, 16 ), '#06b')[2:] for hex_char in lines[0]] )
# sum of versions
versions = []

def extract_chunk ( bin, chunk_length, convert_to_int = False ):
    # return (stripped binary, chunk itself)
    # if convert_binary is true, then the chunk is converted to integer
    if convert_to_int:
        return bin[chunk_length:], int ( bin[:chunk_length], 2 )

    return bin[chunk_length:], bin[:chunk_length]


def extract_literal ( bin ):
    #print ( f" - received for literal extraction: {bin}")
    literal = ""

    # keep extracting until first bit is 0
    while True:
        bin, chunk = extract_chunk ( bin, LITERAL_CHUNK )
        #print ( f"   - extracted chunk: {chunk}, literal: {chunk[1:]}")
        literal += chunk[1:]
        
        if chunk[0] == '0':
            break
    
    print ( f"  - extracted literal: {int(literal,2)}")
    return bin, int ( literal, 2 )


# binary packet contains either literal numbers or list of packets

def parse_packet ( bin ):
    #print ( f"parsing packet: {bin}")

    bin, packet_version = extract_chunk ( bin, VERSION_LENGTH, convert_to_int=True )
    bin, packet_type = extract_chunk ( bin, TYPE_LENGH, convert_to_int=True )

    versions . append ( packet_version )
    
    #print ( f" - packet version: {packet_version}")
    #print ( f" - packet type:    {packet_type}")

    type = "LITERAL" if packet_type == 4 else "OPERATOR"

    print ( f" - received packed type: {type}")
    #print ( f" - remaining BEFORE mode extraction: {bin}")
    if packet_type == 4:
        bin, literal = extract_literal ( bin )
        return bin
    else:
        bin, mode = extract_chunk ( bin, OPERATOR_MODE_LEN, convert_to_int=True )
        #print ( f" - subpackets mode: {mode}")

        if mode == 1:
            bin, packets = extract_chunk ( bin, OPERATOR_PACKET_NUM, convert_to_int=True)

            for i in range ( packets ):
                bin = parse_packet ( bin )
            
        else:
            bin, subpackets_bit_len = extract_chunk ( bin, OPERATOR_BIT_LENGTH, convert_to_int=True )
            bits_parsed = 0

            #print ( f" - length of subpackets: {subpackets_bit_len}")

            while True:
                remaining_bin = parse_packet ( bin )
                bits_parsed += len ( bin ) - len ( remaining_bin )

                bin = remaining_bin

                if bits_parsed >= subpackets_bit_len:
                    break

    return bin

parse_packet ( binary )

print ( f"sum of all version numbers: {sum(versions)}")
