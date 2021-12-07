# description required by advent.py
description = ("Minimize crab submarine fuel, fuel=steps",                     # part 1
               "Minimize crab submarine fuel, fuel=(steps*(steps+1))/2"        # part 2        
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
    
    min_fuel_pos, min_fuel = optimize_crab_fuel(lines[0], puzzle_part=1)
    
    print(f'minimum fuel position={min_fuel_pos}, fuel used={min_fuel}')
       
    
def puzzle_part2(lines):
    """run part2 of puzzle"""
    
    min_fuel_pos, min_fuel = optimize_crab_fuel(lines[0], puzzle_part=2)
            
    print(f'minimum fuel position={min_fuel_pos}, fuel used={min_fuel}')


def optimize_crab_fuel(crabs_line, puzzle_part):
    """find the position to which the crab submarines should move, to minimize fuel use"""
    
    # produce a list of integer positions of the crab submarines
    crabs = [int(crab) for crab in crabs_line.split(',')]
    max_pos = max(crabs)
    min_pos = min(crabs)
    
    # we need to minimize fuel use for the crab submarines
    
    # set the minimum fuel higher than the maximum it could possibly be
    # assume all submarines have to move the maximum distance
    min_fuel = fuel_used_for(max_pos, puzzle_part) * len(crabs)
    min_fuel_pos = None
    
    # for each possible position that all submarines could move to
    # compute the fuel used for that position and remember the position
    # with the minimum fuel used
    for pos in range(min_pos, max_pos):
        # for this position (pos) sum the fuel used to get there by all of the submarines
        fuel_for_this_pos = 0
        for crab in crabs:
            fuel_for_this_pos += fuel_used_for(abs(crab - pos), puzzle_part)
        
        # if this position uses less fuel than any we have already seen, remember it
        if fuel_for_this_pos < min_fuel:
            min_fuel = fuel_for_this_pos
            min_fuel_pos = pos
    
    # return the position using the least fuel, and the amount of fuel used
    return (min_fuel_pos, min_fuel)
    

def fuel_used_for(steps, puzzle_part):  
    """compute fuel used for 'steps' moves"""
    
    # For Part 1 of the puzzle, the fuel used is just the number of steps
    if puzzle_part == 1:
        return steps
    
    # For Part 2 of the puzzle, the fuel used is the sum of the digits from 1 to steps 
    # Use Gauss' formula:
    #   sum = (n*(n+1)) / 2
    return int((steps * (steps + 1)) / 2)
    
    
# import code common for all Advent puzzles
import advent 
# pass module name, and package
advent.startup(__name__, __package__)

