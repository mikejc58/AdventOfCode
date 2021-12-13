# description required by advent.py
description = (("Interpret the user manual by folding",             # part 1
                "apply just the first fold and count the dots"),
               ("Interpret the user manual by folding",             # part 2     
                "apply all the folds and read the resulting code")   
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
        self.prepare_input_list(lines)


    def puzzle_part1(self):
        """run  part1 of puzzle"""
        
        # perform the first fold
        # remove that fold from the list so we won't try to do it again in part2
        axis, index = self.folds.pop(0)
        if axis == 'y':
            self.fold_horizontal(index)
        else:
            self.fold_vertical(index)
        
        print(f"dot count after 1 fold = {self.count_dots()}")
    
    def puzzle_part2(self):
        """run part2 of puzzle"""
        
        # perform the sequence of folds (the first fold has already been done)
        for axis, index in self.folds:
            if axis == 'y':
                self.fold_horizontal(index)
            else:
                self.fold_vertical(index)
                
        # print the grid so we can see the code
        self.print()

    def merge_grid(self, fold_grid):
        """merge the folded and the base parts of the grid)"""
        for y in range(len(self.grid)):
            for x in range(len(self.grid[0])):
                if self.grid[y][x] == '.':
                    self.grid[y][x] = fold_grid[y][x]
        

    def fold_horizontal(self, y_fold):
        """fold the grid on a horizontal axis"""
        # create the folded part of the grid
        fold_grid = self.grid[y_fold*2:y_fold:-1]
        # base grid is reduced to half
        self.grid = self.grid[0:y_fold:]
        
        # merge the folded and base grids
        self.merge_grid(fold_grid)
    
    def fold_vertical(self, x_fold):
        """fold the grid on a vertical axis"""
        # create the folded part of the grid
        fold_grid = [row[x_fold*2:x_fold:-1] for row in self.grid]
        # base grid is reduced to half
        self.grid = [row[:x_fold] for row in self.grid]
            
        # merge the folded and base grids    
        self.merge_grid(fold_grid)    
        
    def count_dots(self):
        """count the number of 'dots' """
        dot_count = 0
        for row in self.grid:
            for point in row:
                if point == '#':
                    dot_count += 1
        return dot_count
        
    def print(self):
        """if small, print the grid, otherwise just print its size"""
        if len(self.grid) > 50:
            print(f"grid size is {len(self.grid[0])},{len(self.grid)}")
        else:
            for row in self.grid:
                for point in row:
                    # to make the code more readable
                    # change the '.' into a space
                    if point == '.': point = ' '
                    # change the '#' into a filled block
                    if point == '#': point = '\u2586'
                    print(f"{point}", end='') 
                print()
        print()
        
    def prepare_input_list(self, lines):
        """create a list of the input"""
        self.points = []
        self.folds = []
        for line in lines:
            if ',' in line:
                # process x,y point
                x, y = line.split(',')
                x = int(x)
                y = int(y)
                self.points.append((x,y))
            elif 'fold' in line:
                # process fold line
                _, _, v = line.split()
                axis, index = v.split('=')
                index = int(index)
                self.folds.append((axis, index))
        
        max_x = 0
        max_y = 0
        for x,y in self.points:
            max_x = max(max_x, x)
            max_y = max(max_y, y)
        
        max_index_x = 0
        max_index_y = 0
        for axis, index in self.folds:
            if axis == 'x':
                max_index_x = max(max_index_x, index)
            else:
                max_index_y = max(max_index_y, index)
        self.x_size = max(max_x, max_index_x * 2) + 1
        self.y_size = max(max_y, max_index_y * 2) + 1
        
        self.grid = [['.' for x in range(self.x_size)] for y in range(self.y_size)]
        for x,y in self.points:
            self.grid[y][x] = '#'
            
        
        
    
# import code common for all Advent puzzles
import advent 
# pass module name, and package
advent.startup(__name__, __package__, obj=True)

