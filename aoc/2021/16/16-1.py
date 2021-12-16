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

# operator modes
class OPERATOR_TYPES:
    SUM     = 0
    PRODUCT = 1
    MIN     = 2
    MAX     = 3
    LITERAL = 4
    GT      = 5
    LT      = 6
    EQ      = 7

# input -- be careful, int is trimming leading zeroes
binary = "". join ( [ format (int ( hex_char, 16 ), '#06b')[2:] for hex_char in lines[0]] )

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
    # print ( f"parsing packet: {bin}")
    numbers = []

    bin, packet_version = extract_chunk ( bin, VERSION_LENGTH, convert_to_int=True )
    bin, packet_type = extract_chunk ( bin, TYPE_LENGH, convert_to_int=True )
    
    #print ( f" - packet version: {packet_version}")
    #print ( f" - packet type:    {packet_type}")

    type = "LITERAL" if packet_type == OPERATOR_TYPES.LITERAL else "OPERATOR"

    print ( f" - received packed type: {type} ({packet_type})")
    #print ( f" - remaining BEFORE mode extraction: {bin}")
    if packet_type == 4:
        bin, literal = extract_literal ( bin )
        return bin, literal
    else:
        bin, mode = extract_chunk ( bin, OPERATOR_MODE_LEN, convert_to_int=True )
        #print ( f" - subpackets mode: {mode}")
        

        if mode == 1:
            bin, packets = extract_chunk ( bin, OPERATOR_PACKET_NUM, convert_to_int=True)

            for i in range ( packets ):
                bin, number = parse_packet ( bin )
                numbers . append ( number )
            
        else:
            bin, subpackets_bit_len = extract_chunk ( bin, OPERATOR_BIT_LENGTH, convert_to_int=True )
            bits_parsed = 0

            #print ( f" - length of subpackets: {subpackets_bit_len}")

            while True:
                remaining_bin, number  = parse_packet ( bin )
                bits_parsed += len ( bin ) - len ( remaining_bin )
                numbers . append ( number )

                bin = remaining_bin

                if bits_parsed >= subpackets_bit_len:
                    break

    # if we got here, it means there are >1 numbers in <numbers>
    match packet_type:
        case OPERATOR_TYPES.SUM:
            return bin, sum ( numbers )
        case OPERATOR_TYPES.PRODUCT:
            prod = 1
            for n in numbers:
                prod *= n
            return bin, prod
        case OPERATOR_TYPES.MIN:
            return bin, min ( numbers )
        case OPERATOR_TYPES.MAX:
            return bin, max ( numbers )
        case OPERATOR_TYPES.GT:
            return bin, 1 if numbers[0] > numbers[1] else 0
        case OPERATOR_TYPES.LT:
            return bin, 1 if numbers[0] < numbers[1] else 0
        case OPERATOR_TYPES.EQ:
            return bin, 1 if numbers[0] == numbers[1] else 0


    return bin

string, result = parse_packet ( binary )
print ( f"result of expression: {result}")
