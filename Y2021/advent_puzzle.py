# description required by test_all.py
description = ("",       # part 1
               ""        # part 2        
              )

# to run:
#   put advent_puzzle.py and advent.py into a folder
#   navigate to that folder
#   execute  python3 advent_puzzle.py

#   advent.py contains functions that are (will be common) to all of the puzzles
#   and advent.py and advent_puzzle.py have some complications because I have set
#   them up to be able to be executed in a batch with more puzzles.  You can ignore
#   that.  

def puzzle(input_file):
    """run part1 and part2 of the puzzle
         parameters are the input file name, and a parameter that
         can be 1 to execute only Part1, 2 to execute only Part2 or 'both' to execute both parts
    """
    
    lines = advent.read_input(input_file, prep_function=None)

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



def puzzle_part1(depths):
    """run  part1 of puzzle"""
    pass
    
def puzzle_part2(lines):
    """run part2 of puzzle"""
    pass
    

# import code common for all Advent puzzles
#    advent.startup
#    advent.read_input
import advent 
# pass module name, and package
advent.startup(__name__, __package__)

