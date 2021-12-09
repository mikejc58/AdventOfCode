# description required by advent.py
description = ("Find all low points in the map and calculate the sum of the risk levels",       # part 1
               ("Find the three biggest basins (around the low points)",
                "and calculate the product of their sizes")                                     # part 2        
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
    
    grid = prepare_input_list(lines)
    
    # iterate over the grid and find all of the 'low points'
    # marked_grid will have True where there is a low point, otherwise False
    low_points_grid = mark_low_points(grid)
    
    # compute sum of the risk values
    # risk value is low_point value + 1
    total_risk = 0
    for y, row in enumerate(low_points_grid):
        for x, low_point in enumerate(row):
            if low_point:
                total_risk += grid[y][x] + 1
    
    if len(grid) < 20:
        print_grid(grid, low_points_grid)
        
    print(f"total risk is {total_risk}")
    

def puzzle_part2(lines):
    """run part2 of puzzle"""
    grid = prepare_input_list(lines)
    
    # iterate over the grid and find all of the 'low points'
    # marked_grid will have True where there is a low point, otherwise False
    low_points_grid = mark_low_points(grid)
    
    # list of the three biggest basin sizes
    biggest_basins = [0, 0, 0]
    
    # iterate over the low points grid, and for each low point compute the basin around it
    for y, row in enumerate(low_points_grid):
        for x, low_point in enumerate(row):
            if low_point:
                # point x,y is a low point, compute the basin around it
                basin_size = compute_basin(grid, (x,y))
                # see if the new basin is bigger than the smallest of the big basins
                if basin_size > biggest_basins[2]:
                    # replace the smallest of the big basins with the new basin
                    biggest_basins[2] = basin_size
                    # sort to get smallest into index 2
                    biggest_basins.sort(reverse=True)
    
    print(f"3 biggest basins are {biggest_basins}")
    
    # compute the product of the three largest basin sizes
    product = 1
    for basin_size in biggest_basins:
        product *= basin_size
    print(f"product of biggesst 3 basin sizes is {product}")


def mark_low_points(grid):
    """build a marked_grid identifying the low points of the grid"""
    max_y = len(grid)-1
    max_x = len(grid[0])-1
    # intialize a marked_grid to all True 
    # in the loop below will will mark everything False that is not a low point
    low_points_grid = make_marked_grid((max_x+1, max_y+1), init_value=True)
    
    for y, row in enumerate(grid):
        for x, val_xy in enumerate(row):
            # for each x,y point, find if it is lower than its four neighbors
            if (x > 0     and grid[y][x-1] <= val_xy) or    \
               (x < max_x and grid[y][x+1] <= val_xy) or    \
               (y > 0     and grid[y-1][x] <= val_xy) or    \
               (y < max_y and grid[y+1][x] <= val_xy):
                low_points_grid[y][x] = False
            
    return low_points_grid
    
    
def prepare_input_list(lines):
    """create a list of lists of the input"""
    return [[int(val) for val in list(line)] for line in lines]
            

def print_grid(grid, marked_grid):
    """print the grid, highlighting the marked points"""
    for line, marks in zip(grid, marked_grid):
        for val, mark in zip(line, marks):
            mark = advent.BRIGHT if mark else advent.DIM
            print(f"{mark}{val}{advent.NORMAL}", end='')
        print()
    print()


def make_marked_grid(xy_size, init_value=False):
    """build a grid marked with the initial value"""
    size_x, size_y = xy_size
    return [[init_value for _ in range(size_x)] for _ in range(size_y)]
    
    
def compute_basin(grid, low_point):
    """compute the size of the basin around the low point"""
    x, y = low_point
    xy_size = (len(grid[0]), len(grid)) 
    
    # make a grid to keep track of the basin's points
    basin_grid = make_marked_grid((len(grid[0]), len(grid)), init_value = False)
    
    # add the low point to the basin
    #  this will recursively add all of the points
    #  which are within the basin
    add_to_basin(grid, (x,y), basin_grid, xy_size)
    
    # now compute size of the basin
    basin_size = 0
    for row in basin_grid:
        for basin_point in row:
            if basin_point:
                basin_size += 1
    
    if len(grid) < 20:            
        print_grid(grid, basin_grid)
    
    return basin_size
    
    
def add_to_basin(grid, xy, basin_grid, xy_size):
    """recursively add a point to the basin"""
    x, y = xy
    x_size, y_size = xy_size
    
    # add the point at x,y to the basin
    basin_grid[y][x] = True
    
    # try to add the points in the 4 directions from this point
    #  points beyond the edges of the grid are ignored
    if x > 0:
        possibly_add_to_basin(grid, (x-1,y), basin_grid, xy_size)
    if x < x_size-1:
        possibly_add_to_basin(grid, (x+1,y), basin_grid, xy_size)
    if y > 0:
        possibly_add_to_basin(grid, (x,y-1), basin_grid, xy_size)
    if y < y_size-1:
        possibly_add_to_basin(grid, (x,y+1), basin_grid, xy_size)
    
    
def possibly_add_to_basin(grid, xy, basin_grid, xy_size):
    """test if the specified point can be added to the basin"""
    x, y = xy
    
    # if x,y is already in the basin, do not add it again
    if not basin_grid[y][x]:
        # height of 9 terminates the basin
        if grid[y][x] != 9:
            # add this point to the basin
            #  this will recursively add the points 
            #  in the four directions from this point
            add_to_basin(grid, xy, basin_grid, xy_size)
        

# import code common for all Advent puzzles
import advent 
# pass module name, and package
advent.startup(__name__, __package__)

