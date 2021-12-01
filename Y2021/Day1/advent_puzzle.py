# description required by test_all.py
description = ("count the number of times a depth measurement increases",       # part 1
               "count the number of times the sum of measurements\n         \
               in sliding windows increases"                                    # part 2        
              )

# to run:
#   put advent_puzzle.py and advent.py into a folder
#   navigate to that folder
#   execute  python3 advent_puzzle.py

#   advent.py contains functions that are (will be) common to all of the puzzles
#   and advent.py and advent_puzzle.py have some complications because I have set
#   them up to be able to be executed in a batch with more puzzles.  You can ignore
#   that.  

def puzzle(input_file, part='both'):
    """run part1 and part2 of the puzzle
         parameters are the input file name, and a parameter that
         can be 1 to execute only Part1, 2 to execute only Part2 or 'both' to execute both parts
    """
    
    # read the input lines, convert them to integers and put them in a list of lines
    lines = advent.read_input(input_file, prep_function=lambda line: int(line))
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
    
    # number of times depth increased
    increase_count = 0
    
    prev_depth = None
    for depth in depths:
        if prev_depth is not None and depth > prev_depth:
            increase_count += 1
        prev_depth = depth
        
    print(f"\ndepth increased {increase_count} times\n")


def puzzle_part2(depths):
    """run part2 of puzzle"""
    
    # number of times depth increased in 3-measurement windows
    increase_count = 0
    
    # first sum is for depths[0]+depths[1]+depths[2] (window A in the puzzle)
    previous_sum = sum(depths[0:3])
    
    # loop for each of the following 3-element windows (window B through the end)
    for i in range(4, len(depths)+1):
        current_sum = sum(depths[i-3:i])
        if current_sum > previous_sum:
            increase_count += 1
        previous_sum = current_sum
    
    print(f"\ndepth increased {increase_count} times\n")



# import code common for all Advent puzzles
#    advent.startup
#    advent.read_input
import advent 
# pass module name, and package
advent.startup(__name__, __package__)

