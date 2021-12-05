# description required by advent.py
"""This is doc line 1"""
"""This is doc line 2"""
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


def puzzle_part1(lines):
    """run  part1 of puzzle"""
    
    depths = prepare_input_list(lines)
    
    # number of times depth increased
    increase_count = 0
    
    prev_depth = None
    for depth in depths:
        if prev_depth is not None and depth > prev_depth:
            increase_count += 1
        prev_depth = depth
        
    print(f"\ndepth increased {increase_count} times\n")


def puzzle_part2(lines):
    """run part2 of puzzle"""
    
    depths = prepare_input_list(lines)
    
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

def prepare_input_list(lines):
    return [int(line) for line in lines]

# import code common for all Advent puzzles
import advent 
# pass module name, and package
advent.startup(__name__, __package__, )

