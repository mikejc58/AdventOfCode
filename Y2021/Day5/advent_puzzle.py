# description required by advent.py
description = ("Horizontal and Vertical lines overlap at how many points?",       # part 1
               "Horizontal, Vertical and Diagonal lines this time"                # part 2        
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
    lines = prepare_input_list(lines)
    
    find_overlap(lines, include_diagonal=False)
                
                    
def puzzle_part2(lines):
    """run part2 of puzzle"""
    
    lines = prepare_input_list(lines)
    
    find_overlap(lines, include_diagonal=True)


def find_overlap(lines, include_diagonal):
    """find the overlapping lines in the input"""
    
    # enable display of final grid for small input files
    if len(lines) < 20:
        show_grid = True
    else:
        show_grid = False
        
    # find the maximum size of the grid
    max_x = 0
    max_y = 0
    for line in lines:
        x0, y0 = line[0]
        x1, y1 = line[1]
        max_x = max(max_x, x0, x1)
        max_y = max(max_y, y0, y1)
    print(f"max x,y = ({max_x}, {max_y})")
    
    # build a grid with max_y rows and max_x columns.  Each point starts at zero and is incremented
    # for each line that goes through the point.
    grid = [[0 for _ in range(max_x+1)] for _ in range(max_y+1)]
    
    # process the lines and add them to the grid    
    for line in lines:
        # validate each line (must be horizontal, vertical or optionally diagonal)    
        xy_data = is_valid(line, include_diagonal=include_diagonal)
        if xy_data:
            # it is a valid line to be added
            # get the information computed by is_valid
            (x, increment_x), (y, increment_y), line_range = xy_data
            
            # add each of the lines' points to the grid
            while line_range >= 0:
                grid[y][x] += 1
                x += increment_x
                y += increment_y
                line_range -= 1
                
        # the line did not meet the criteria        
        else:
            continue
    
    # now count how many points on the grid had more than one line crossing it        
    overlaps = 0
    for row in grid:
        for count in row:
            if count > 1:
                overlaps += 1
            if show_grid:
                if count:
                    print(f"{count:2d}", end='')
                else:
                    print(' .', end='')
        if show_grid:
            print()
            
    # display the puzzle result
    print(f"count of overlaps>1 = {overlaps}")

    
def prepare_input_list(lines):
    """convert the input lines into a list of line points"""
    lines_ints = []
    for line in lines:
        parts = line.split()
        linestart = tuple([int(v) for v in parts[0].split(',')])
        lineend = tuple([int(v) for v in parts[2].split(',')])
        lines_ints.append((linestart, lineend))
    return lines_ints

def is_valid(line, include_diagonal=False):
    """check if line is a valid horizontal, vertical or diagonal line
       and return the information needed to draw the line"""
    
    # get the x,y endpoints of the line
    x0, y0 = line[0]
    x1, y1 = line[1]
    
    # change in x and change in y for the line   
    delta_x = x1 - x0  
    delta_y = y1 - y0  
    
    # length in x and y direction
    range_x = abs(delta_x)
    range_y = abs(delta_y)
    
    # steps in x and y direction
    increment_x = 0
    increment_y = 0
    
    # compute the increment (-1, 0, or +1) for x and y
    # set the 'length' of the line
    #  note: if range_x and range_y are both greater than zero
    #        we set the line_range from range_y only.  This is
    #        okay because: if both range_x and range_y are non-zero 
    #        then they must be equal to each other in order for the
    #        line to be considered valid.
    if range_x > 0:
        line_range = range_x
        increment_x = int(delta_x / range_x)
    if range_y > 0:
        line_range = range_y
        increment_y = int(delta_y / range_y)
    
    # build the tuple to be returned to the caller
    xy_data = ((x0, increment_x), (y0, increment_y), line_range)
    
    # line is valid if range_x is 0 (vertical) or range_y is 0 (horizontal)
    #  or if including diagonals, if range_x is the same as range_y
    if range_x == 0 or range_y == 0 or (include_diagonal and (range_x == range_y)):
        return xy_data
    
    # line did not meet the criteria    
    return None
    
    
# import code common for all Advent puzzles
import advent 
# pass module name, and package
advent.startup(__name__, __package__)

