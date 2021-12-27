# description required by advent.py
description = (("Execute reactor reboot procedure, turning cubes on and off",       # part 1
                "but only for cubes with ranges within -50::50",        # part 1
                "After the procedure, how many cubes in the initialization area are on?"),
               ("Execute reactor reboot procedure, turning cubes on and off",       # part 2       
                "for all cubes in the input",          
                "After the procedure, how many cubes are on?") 
              )
import copy
from dataclasses import dataclass

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
        self.commands = self.prepare_input_list(lines)


    def puzzle_part1(self):
        """run  part1 of puzzle"""
        # save the original set of commands for part2
        old_commands = self.commands
        new_commands = []
        # remove any commands that have coordinates outside of -50::50
        for command in self.commands:
            keep = True
            cmd, coords = command
            for v in coords:
                if v[0] < -50 or v[1] > 50:
                    keep = False
            if keep:
                new_commands.append(command)
        self.commands = new_commands
        # now run the puzzle_part2 algorithm with the restricted set of commands
        self.puzzle_part2()
        
        # restore the original commands
        self.commands = old_commands
        
        
    def puzzle_part2(self):
        """run part2 of puzzle"""
        total_on = 0
        # list of 'previous' cubes to which the new cubes are applied
        # cube_list is organized as a 'push down' stack, the most recent
        # cube is inserted into position 0
        # subsequent cubes are tested against cube_list[0], then cube_list[1], etc.
        cube_list = []
        for cmd, coords in self.commands:
            new_cube = Cube(Range(*coords[0]), Range(*coords[1]), Range(*coords[2]), cmd)
            # residual_cubes is the set of remaining cubes that need to be applied to
            # previous cubes
            # the new_cube starts as the only member of residual_cubes
            residual_cubes = [new_cube]
            for cube1 in cube_list:
                # work back through the previous cubes, finding overlaps and applying the changes
                # next_residual_cubes will become residual_cubes for the next iteration (previous cube1)
                next_residual_cubes = []
                for cube2 in residual_cubes:
                    overlap, residual = findoverlap3D(cube1, cube2)
                    if overlap is None:
                        # cube2 doesn't overlap with this cube1 from
                        # the list, but it may overlap with earlier
                        # cubes.  So add it to the next residuals
                        # so it will be tested against earlier cubes
                        next_residual_cubes.append(cube2)
                    else:
                        # apply overlap.cmd to the overlap with cube1.cmd
                        if overlap.cmd == 'on' and cube1.cmd == 'off':
                            total_on += overlap.size()
                        elif overlap.cmd == 'off' and cube1.cmd == 'on':
                            total_on -= overlap.size()
                        # add new residuals (parts of cube2 that didn't overlap) to next_residuals
                        next_residual_cubes += residual
                residual_cubes = next_residual_cubes  
                
            # if there are any residual cubes left, apply them to the background
            for cube in residual_cubes:
                if cube.cmd == 'on':
                    total_on += cube.size() 
                      
            # finally, add new_cube to cube_list
            cube_list.insert(0, new_cube)
    
        print(f"total on = {total_on}")
    
    
    def prepare_input_list(self, lines):
        """create a list of the input"""
        commands = []
        for line in lines:
            cmd, line = line.split()
            line = line.split(',')
            coords = [v.split('=')[1] for v in line]
            coords = [v.split('..') for v in coords]
            coords = tuple([tuple([int(v) for v in coord]) for coord in coords])
            commands.append((cmd, coords))
        
        return tuple(commands)



def findoverlap3D(cube1:'Cube', cube2:'Cube'):
    """find any overlap between cube1 and cube2 
    
       if there is no overlap, return None for the overlap,
       and cube2 for the residual (which will then be tested against
       the 'previous' cube)
       
       if there is an overlap, return the overlap which will be applied
       to cube1, and the residual cubes (0 to 26) which will be tested against
       the 'previous' cube
    """
    # find the overlap and the residuals
    splits = get_splits(cube1, cube2)
    if splits is None:
        # there was no overlap
        # overlap None, residuals is cube2
        return (None, [cube2,])
        
    else:
        # there was an overlap
        x_split, y_split, z_split = splits
        
        cubes = [cube for cube in generate_cubes(splits, cube2.cmd)]
        # the first cube generated is the overlap
        overlap_cube = cubes[0]
        # the rest are the residuals that did not overlap
        residual_cubes = cubes[1:]
            
        return (overlap_cube, residual_cubes)
    

def generate_cubes(splits, cmd):
    """generate the 'cubes' from the splits"""
    # there may be from 1 to 27 cubes generated here depending on the overlaps
    # the first cube generated will be the overlap, the rest are the 'residuals'
    x_split, y_split, z_split = splits
    for x in x_split:
        for y in y_split:
            for z in z_split:
                if x is not None and y is not None and z is not None:
                    yield Cube(x, y, z, cmd)


def get_splits(cube1:'Cube', cube2:'Cube'):
    """find the overlaps and split ranges for x, y and z"""
    # get the Range objects from the cubes
    x1, y1, z1 = cube1
    x2, y2, z2 = cube2
    
    # for the cubes to overlap, they must have overlaps in all three ranges (x, y and z)
    x_split = find_overlap1D(x1,x2)
    if x_split is None:
        # if there is no overlap in the x ranges, then the cubes do not overlap
        return None
        
    y_split = find_overlap1D(y1,y2)
    if y_split is None:
        # if there is no overlap in the y ranges, then the cubes do not overlap
        return None
        
    z_split = find_overlap1D(z1,z2)
    if z_split is None:
        # if there is no overlap in the z ranges, then the cubes do not overlap
        return None
        
    # the cubes overlap, return the splits
    return (x_split, y_split, z_split)
    
        
@dataclass
class Range:
    """class to hold a one dimensional range"""
    start : int
    end   : int
    
    def length(self):
        return (self.end - self.start) + 1
        
    def __iter__(self):
        yield from (self.start, self.end)
        
    def __str__(self):
        return f"({self.start}::{self.end})"
        
    def __repr__(self):
        return self.__str__()
    
    
@dataclass(frozen=True)
class SplitRange:
    """class to hold a range split into 3 parts"""
    overlap : Range = None
    minus   : Range = None
    plus    : Range = None
    
    def __iter__(self):
        yield from (self.overlap, self.minus, self.plus)
        
    
def find_overlap1D(range1:'Range', range2:'Range'):
    """find overlap between range1 and range2"""
    # return overlap, left remaining section, right remaining section
    range1start, range1end = range1
    range2start, range2end = range2
    overlap = None
    minus = None
    plus = None
    # test for overlap
    if range1start <= range2end and range1end >= range2start:
        # the ranges do overlap
        # compute the overlap range  
        overlapstart = max(range1start, range2start)
        overlapend = min(range1end, range2end)    
        overlap = Range(max(range1start, range2start), min(range1end, range2end))
        
        # compute the non-overlapping part of range2 which is less than range1
        if range2start < overlapstart:
            minus = Range(range2start, range1start-1)
        
        # compute the non-overlapping part of range2 which is greater than range1    
        if range2end > overlapend:
            plus = Range(range1end+1, range2end)
        
        # return the split range
        return SplitRange(overlap, minus, plus)   
        
    # there was no overlap, return None
    return None


class Cube:
    """class to hold a 'cube' (really a right-rectangular-prism)
       a Cube consists of an x, y and z range and a command which is 'on' or 'off'
    """
    def __init__(self, x:'Range', y:'Range', z:'Range', cmd:'str'):
        self.x = x
        self.y = y
        self.z = z
        self.cmd = cmd
        
    def __iter__(self):
        yield from (self.x, self.y, self.z)
        
    def size(self):
        return self.x.length() * self.y.length() * self.z.length()
        
    def __str__(self):
        return f"Cube ({self.x},{self.y},{self.z}), cmd={self.cmd}, size={self.size()}"
        
    def __repr__(self):
        return self.__str__()

# import code common for all Advent puzzles
import advent 
# pass module name, and package
advent.startup(__name__, __package__, obj=True)

