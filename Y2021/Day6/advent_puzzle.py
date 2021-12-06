# description required by advent.py
description = ("Calculate Lanternfish after 80 days",        # part 1
               "Calculate Lanternfish after 256 days"        # part 2        
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
    
    total_fish = fish_descendants(lines[0], 80)
        
    print(f"total fish after  80 days {total_fish}")


def puzzle_part2(lines):
    """run part2 of puzzle"""

    total_fish = fish_descendants(lines[0], 256)
        
    print(f"total fish after 256 days {total_fish}")
        
def fish_descendants(fish_string, days):
    """compute number of fish after 'days' """
    # convert the single input line into a list of integers, one for each fish, and which 
    # contain the time (in days) until the fish will spawn
    initial_fish = [int(fish) for fish in fish_string.split(',')]
    
    # current_fish will contain the count of how many fish exist of each possible spawn time
    current_fish = [0] * 9
    for fish in initial_fish:
        current_fish[fish] += 1
    
    # for a given spawn_time, spawn_update gives the spawn_time value(s) for the next day
    #   spawn time    0     1    2    3    4    5    6    7    8
    spawn_updates = ((6,8),(0,),(1,),(2,),(3,),(4,),(5,),(6,),(7,))
    
    # update current_fish to contain the number of fish of each spawn_time after the number of days specified
    for _ in range(days):
        # each day we build a new list with counts of the fish of each possible spawn time (0 - 8)
        next_fish = [0] * 9
        # current_fish contains 9 entries, one for each possible spawn time (0 - 8)
        # the values of these 9 entries contain the number of fish that currently exist
        # with that spawn time.
        
        # spawn_updates contains 9 entries, one for each possible spawn time (0 - 8)
        # the values of these 9 entries contain the spawn times for the next day
        
        # for each of those counts we determine what the next spawn time will be (current-1 for spawn times 
        # greater than 0, and 6 for a spawn time of 0) and move those counts to the new spawn time in next_fish.
        # Also, in the case of current==0, we add the count of fish to spawn time of 8, representing the
        # newly spawned fish.
        # 
        for updates, fish in zip(spawn_updates, current_fish):
            for i in updates:
                next_fish[i] += fish
        # make the next list become the current list
        current_fish = next_fish
    
    # return the total number of fish
    return sum(current_fish)
    
    
 
    
# import code common for all Advent puzzles
import advent 
# pass module name, and package
advent.startup(__name__, __package__)

