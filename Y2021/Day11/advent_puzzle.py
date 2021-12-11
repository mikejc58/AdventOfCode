# description required by advent.py
description = (("Flashing Octopus automaton", "Count the total flashes in 100 steps"),                           # part 1
               ("Flashing Octopus automaton", "How many steps before all octopuses flash simultaneously?")       # part 2        
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
        self.lines = lines


    def puzzle_part1(self):
        """run  part1 of puzzle"""
        self.grid = self.prepare_input_list(self.lines)
        
        self.print_grid("Initial grid")
        steps = 100
        total_flashes = 0
        for i in range(steps):
            
            total_flashes += self.step_grid()
            if (i+1) % 10 == 0:
                self.print_grid(f"After Step {i+1}")
            
        print(f"Total flashes = {total_flashes}")
    
    
    def puzzle_part2(self):
        """run part2 of puzzle"""
        self.grid = self.prepare_input_list(self.lines)
        
        self.print_grid("Initial grid")
        steps = 600
        total_flashes = 0
        for i in range(steps):
            
            flashes = self.step_grid()
            total_flashes += flashes
            if flashes == 100:
                self.print_grid(f"After Step {i+1} with {flashes} flashes")
                break
            if (i+1) % 10 == 0:
                self.print_grid(f"After Step {i+1} with {flashes} flashes")
            
        print(f"Total flashes = {total_flashes}")


    def step_grid(self):
        """perform one step on the grid"""
        
        # first increment the energy levels of each octopus
        self.step_part1()
        
        # find octopuses with energy > 9, and flash their neighbors
        total_flashes = 0
        flashes = 1
        # keep looping here until no more flashes detected
        while flashes != 0:
            # find any octopuses that have energy > 9 and make them flash
            flashes = self.step_part2()
            total_flashes += flashes
            
            # for each that flashed, we need to increase the energy of its neighbors
            if flashes > 0:
                self.step_part3()
                
        return total_flashes
        
        
    def octopus_grid(self):
        """generate x, y, and val for each octopus in the grid"""
        for y, row in enumerate(self.grid):
            for x, val in enumerate(row):
                yield x, y, val
                
                
    neighbors_set = ((-1,-1),(0,-1),(1,-1),(-1,0),(1,0),(-1,1),(0,1),(1,1))

    def neighbors(self, x, y):
        """generate coordinates for neighbors of octopus at x,y """
        
        for dx, dy in AdventPuzzle.neighbors_set:
            # compute x, y coordinates of each of the eight neighbors
            xp, yp = x+dx, y+dy
            # if the neighbor is within the grid return its coordinates
            if 0 <= xp < 10 and 0 <= yp < 10:
                yield xp, yp
                
        
    def step_part1(self):
        """increase each octopus by 1"""
        for x, y, val in self.octopus_grid():
            self.grid[y][x] = val + 1
        
        
    def step_part2(self):
        """find octopuses with energy greater than 9, and set them to -1 (which indicates about to flash)"""
        flashes = 0
        for x, y, val in self.octopus_grid():
            if val > 9:
                self.grid[y][x] = -1
                flashes += 1
        return flashes
        
        
        
    def step_part3(self):
        """find any octopus with energy = -1 (about to flash), set it to 0 (flashed) and increase its neighbors by 1"""
        for x, y, val in self.octopus_grid():
            if val == -1:
                # set the energy of the octopus that just flashed to 0
                self.grid[y][x] = 0
                for xp, yp in self.neighbors(x, y):
                    # do not increase neighbor if it's energy is zero (just flashed) or -1 (about to flash)
                    if self.grid[yp][xp] > 0:
                        self.grid[yp][xp] += 1


    def print_grid(self, title=None):
        """print the grid, highlighting any octopuses that just flashed (energy=0)"""
        if title:
            print(title)
        for row in self.grid:
            for val in row:
                if val == 0:
                    bright = advent.BRIGHT
                else:
                    bright = advent.DIM
                print(f"{bright}{val}{advent.NORMAL}", end='')
            print()
        print('\n')
                        
        
    def prepare_input_list(self, lines):
        """create a list of the input"""
        return [[int(v) for v in line] for line in lines]
    
# import code common for all Advent puzzles
import advent 
# pass module name, and package
advent.startup(__name__, __package__, obj=True)

