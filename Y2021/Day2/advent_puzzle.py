# description required by advent.py
description = ("product of final horizontal position and final depth",       # part 1
               "product of final horizontal position and final depth"        # part 2        
              )

# to run:
#   put advent_puzzle.py and advent.py into a folder
#   navigate to that folder
#   execute  python3 advent_puzzle.py

#   advent.py contains functions that are (will be common) to all of the puzzles
#   and advent.py and advent_puzzle.py have some complications because I have set
#   them up to be able to be executed in a batch with more puzzles.  You can ignore
#   that.  


def puzzle_part1(lines):
    """run  part1 of puzzle"""
    commands = prepare_input_list(lines)
    horizontal = 0
    depth = 0
    for cmd, val in commands:
        if cmd == 'forward':
            horizontal += val
        elif cmd == 'down':
            depth += val
        elif cmd == 'up':
            depth -= val
        else:
            print(f"invalid command '{cmd}'")
            
    print(f"final horizontal position={horizontal}, final depth={depth}")
    print(f"product={horizontal * depth}")
        
        
        
def puzzle_part2(lines):
    """run part2 of puzzle"""
    commands = prepare_input_list(lines)
    horizontal = 0
    depth = 0
    aim = 0
    for cmd, val in commands:
        if cmd == 'forward':
            horizontal += val
            depth += aim * val
        elif cmd == 'down':
            aim += val
        elif cmd == 'up':
            aim -= val
        else:
            print(f"invalid command '{cmd}'")
            
    print(f"final horizontal position={horizontal}, final depth={depth}, aim={aim}")
    print(f"product={horizontal * depth}")
    

def prepare_input_list(lines):
    """convert each line into a list with a command and a number"""
    
    return [[cmd, int(number)] for (cmd, number) in (line.rstrip().split() for line in lines)]


# import code common for all Advent puzzles
import advent 
# pass module name, and package
advent.startup(__name__, __package__)

