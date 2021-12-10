# description required by advent.py
description = ( "Find all low points in the map and calculate the sum of the risk levels",       # part 1
               ("Find the three biggest basins (around the low points)",
                "and calculate the product of their sizes")                                      # part 2        
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
        self.y_size = len(self.grid)
        self.x_size = len(self.grid[0])
        
        # iterate over the grid and find all of the 'low points'
        # marked_grid will have True where there is a low point, otherwise False
        self.low_points_grid = self.mark_low_points()

    def puzzle_part1(self):
        """run  part1 of puzzle"""
        
        # compute sum of the risk values
        # risk value is low_point value + 1
        total_risk = 0
        for y, row in enumerate(self.low_points_grid):
            for x, low_point in enumerate(row):
                if low_point:
                    total_risk += self.grid[y][x] + 1
        
        # if the grid is small, show the low points
        if self.x_size < 20:
            self.print_grid(self.low_points_grid)
            
        print(f"total risk is {total_risk}")
    
    def puzzle_part2(self):
        """run part2 of puzzle"""
        
        # list of the basin sizes
        basin_sizes = []
        
        # iterate over the low points grid, and for each low point compute the basin around it
        for y, row in enumerate(self.low_points_grid):
            for x, low_point in enumerate(row):
                if low_point:
                    # point x,y is a low point, compute the basin around it
                    basin_sizes.append(self.compute_basin((x,y)))
                    
        basin_sizes.sort(reverse=True)
        print(f"3 biggest basins are {basin_sizes[:3]}")
        
        # compute the product of the three largest basin sizes
        product = 1
        for basin_size in basin_sizes[:3]:
            product *= basin_size
        print(f"product of biggesst 3 basin sizes is {product}")


    @staticmethod
    def prepare_input_list(lines):
        """create a list of lists of the input"""
        return [[int(val) for val in list(line)] for line in lines]
    
    
    def print_grid(self, marked_grid):
        """print the grid, highlighting the marked points"""
        if marked_grid:
            for line, marks in zip(self.grid, marked_grid):
                for val, mark in zip(line, marks):
                    mark = advent.BRIGHT if mark else advent.DIM
                    print(f"{mark}{val}{advent.NORMAL}", end='')
                print()
            print()
        else:
            for line in self.grid:
                for val in line:
                    print(f"{val}", end='')
                print()
            print()
            
            
    deltas = ((-1,0), (+1,0), (0,-1), (0,+1))

    def mark_low_points(self):
        """build a marked_grid identifying the low points of the grid"""
        max_y = self.y_size-1
        max_x = self.x_size-1
        # intialize a marked_grid to all True 
        # in the loop below will will mark everything False that is not a low point
        low_points_grid = self.make_marked_grid(init_value=True)
        
        for y, row in enumerate(self.grid):
            for x, val_xy in enumerate(row):
                # for each x,y point, find if it is lower than its four neighbors
                #  AdvemtPuzzles.deltas contains the offsets for each of the four neighbors
                #  make sure that the neighbor is acutally in the grid
                for dx, dy in AdventPuzzle.deltas:
                    xp, yp = x+dx, y+dy
                    if (0 <= xp < self.x_size) and            \
                       (0 <= yp < self.y_size) and            \
                       (self.grid[yp][xp] <= val_xy):
                        # if the neighbor is less or equal, mark as not a low point
                        low_points_grid[y][x] = False
                
        return low_points_grid


    def make_marked_grid(self, init_value=False):
        """build a grid marked with the initial value"""
        return [[init_value for _ in range(self.x_size)] for _ in range(self.y_size)]
    

    def compute_basin(self, low_point):
        """compute the size of the basin around the low point"""
        x, y = low_point
        
        # make a grid to keep track of the basin's points
        basin_grid = self.make_marked_grid(init_value=False)
        
        # add the low point to the basin
        #  this will recursively add all of the points
        #  which are within the basin
        self.add_to_basin((x,y), basin_grid)
        
        # now compute size of the basin
        basin_size = 0
        for row in basin_grid:
            for basin_point in row:
                if basin_point:
                    basin_size += 1
        
        # if the grid is small, show the basin
        if self.x_size < 20:            
            self.print_grid(basin_grid)
        
        return basin_size


    def add_to_basin(self, xy, basin_grid):
        """add a point, and (recursively) its neighbors, to the basin"""
        x, y = xy
        
        # add the point at x,y to the basin
        basin_grid[y][x] = True
        
        # try to add the points in the 4 directions from this point
        #  points beyond the edges of the grid are ignored
        for dx, dy in AdventPuzzle.deltas:
            self.try_add_to_basin((x+dx,y+dy), basin_grid)


    def try_add_to_basin(self, xy, basin_grid):
        """test if the specified point can be added to the basin
           and add it if it can be
        """
        x, y = xy
        # if the point is within the grid
        #   and it is not already in the basin
        #   and its value is not 9 (9's are not in basins)
        if 0 <= x < self.x_size and         \
           0 <= y < self.y_size and         \
           not basin_grid[y][x] and         \
           self.grid[y][x] != 9 :
            self.add_to_basin(xy, basin_grid)
    
    
# import code common for all Advent puzzles
import advent 
# pass module name, and package
advent.startup(__name__, __package__, obj=True)

