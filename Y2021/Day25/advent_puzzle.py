# description required by advent.py
description = (("Move the seq cucumbers until they can't move any more",        # part 1
                "Determine how many steps go by before they can't move"),
               ("",        # part 2       
                "") 
              )
import copy

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

    def any_movement(self, grid):
        """return True if the two grids differ, else False"""
        for grid_row, self_row in zip(grid, self.grid):
            if grid_row != self_row:
                return True
        return False

    def print(self, grid=None):
        """print the grid"""
        if grid == None:
            grid = self.grid
        for line in grid:
            for c in line:
                print(c, end='')
            print()
        print()

    def puzzle_part1(self):
        """run  part1 of puzzle"""
        for steps in range(1,60000):
            if steps % 100 == 0:
                print(f"{steps} executed")
            half_step = self.step_east(self.grid)
            full_step = self.step_south(half_step)
            if not self.any_movement(full_step):
                print(f"no movement after {steps} steps")
                break
            self.grid = full_step
        
    def step_east(self, grid):
        """move the eastbound sea cucumbers"""
        ll = len(grid[0])
        
        new_grid = []
        for line in grid:
            new_line = copy.copy(line)
            for i, c in enumerate(line):
                if c == '>':
                    # this location contains an eastbound sea cucumber
                    # compute its target location
                    tgt = i+1
                    if tgt == ll:
                        tgt = 0
                    if line[tgt] == '.':
                        # the target location is empty so move
                        new_line[tgt] = '>'
                        new_line[i] = '.'
            new_grid.append(new_line)
        return new_grid

    def step_south(self, grid):
        """move the southbound sea cucumbers"""
        l_row = len(grid[0])
        l_col = len(grid)
        new_grid = copy.deepcopy(grid)
        
        for col in range(l_row):
            for row in range(l_col):
                c = grid[row][col]
                if c == 'v':
                    # this location contains a southbound sea cucumber
                    # compute its target location
                    tgt = row+1
                    if tgt == l_col:
                        tgt = 0
                    if grid[tgt][col] == '.':
                        # the target location is empty so move
                        new_grid[tgt][col] = 'v'
                        new_grid[row][col] = '.'
        return new_grid
    
    def puzzle_part2(self):
        """run part2 of puzzle"""
        
        
    def prepare_input_list(self, lines):
        """create a list of the input"""
        
        grid = [[c for c in line] for line in lines]
            
        return grid
    
# import code common for all Advent puzzles
import advent 
# pass module name, and package
advent.startup(__name__, __package__, obj=True)

