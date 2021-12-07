# description required by advent.py
description = ("count depth increases",                                         # part 1
               "count depth increases for three line sliding windows",          # part 2
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
    
    # count increases in depth for each line (window_size=1)
    increase_count = count_depth_increases(lines, window_size=1)
    
    print(f"\ndepth increased {increase_count} times\n")


def puzzle_part2(lines):
    """run part2 of puzzle"""
    
    # count increases in depth for each window of size 3
    increase_count = count_depth_increases(lines, window_size=3)
    
    print(f"\ndepth increased {increase_count} times\n")


def count_depth_increases(lines, window_size):
    """count depth increases for a window_size window"""
    
    # convert list of strings to a list of integers
    depths = prepare_input_list(lines)
    
    # number of times depth increased in windows of size 'window_size'
    increase_count = 0
    
    # first sum is for the first measurement window
    previous_sum = sum(depths[0:window_size])
    
    # loop for each of the following windows
    for i in range(window_size+1, len(depths)+1):
        current_sum = sum(depths[i-window_size:i])
        if current_sum > previous_sum:
            increase_count += 1
        previous_sum = current_sum
        
    return increase_count


def prepare_input_list(lines):
    """convert the lines to integers"""
    
    return [int(line) for line in lines]

# import code common for all Advent puzzles
import advent 
# pass module name, and package
advent.startup(__name__, __package__, )

