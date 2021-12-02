# description required by test_all.py
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

def puzzle(input_file, part='both'):
    """run part1 and part2 of the puzzle
         parameters are the input file name, and a parameter that
         can be 1 to execute only Part1, 2 to execute only Part2 or 'both' to execute both parts
    """
    
    # read the input file
    lines = advent.read_input(input_file)
    
    # convert each line into a list with a command and a number
    for i, line in enumerate(lines):
        line = line.rstrip()        # get rid of '\n' at the end of the line
        line = line.split()         # split line into ['cmd', 'number']
        line[1] = int(line[1])      # convert number to integer 
        lines[i] = line             # replace the original line with the new list
    
    if part != 'both':
        print('-'*80)
    print(f"{len(lines)} Lines read from {input_file}")
    print('-'*80)

    if part == 1 or part == 'both':
        print(f"\nPart 1 - {description[0]}")
        puzzle_part1(list(lines))
        
    if part == 'both':
        print('-'*80)
    
    if part == 2 or part == 'both':
        print(f"\nPart 2 - {description[1]}")
        puzzle_part2(list(lines))



def puzzle_part1(commands):
    """run  part1 of puzzle"""
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
        
        
        
def puzzle_part2(commands):
    """run part2 of puzzle"""
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
    

# import code common for all Advent puzzles
#    advent.startup
#    advent.read_input
import advent 
# pass module name, and package
advent.startup(__name__, __package__)

