# description required by advent.py
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


class AdventPuzzle():
    def __init__(self, lines):
        """initialize the AdventPuzzle object"""
        self.grid = self.prepare_input_list(lines)


    def puzzle_part1(self):
        """run  part1 of puzzle"""
        pass
        
    
    def puzzle_part2(self):
        """run part2 of puzzle"""
        pass
        
    def prepare_input_list(self, lines):
        """create a list of the input"""
        return lines
    
# import code common for all Advent puzzles
import advent 
# pass module name, and package
advent.startup2(__name__, __package__)

