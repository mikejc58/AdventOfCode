# description required by advent.py
description = (("Find all possible paths through the caves",                    # part 1
                "which may use small (lowercase) caves no more than once"),
               ("Find all possible paths through the caves",                    # part 2   
                "which may use exactly one small cave twice")     
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
        self.caves = self.prepare_input_list(lines)


    def puzzle_part1(self):
        """run  part1 of puzzle"""
        # paths from start to end will be added to self.paths
        self.paths = []
        
        # follow all paths that start with 'start' and end with 'end'
        # small (lowercase) caves can only be used once, large (uppercase)
        # caves can be used any number of times on each path
        path = self.follow_path('start', [])
        
        self.part1_count = len(self.paths)
        print(f"{self.part1_count:6d} paths found:")
        print()
        
        # for small sample data, print the paths found
        if len(self.paths) < 30:
            for path in self.paths:
                AdventPuzzle.print_caves(path)
                print()
            print()
            
            
    def puzzle_part2(self):
        """run part2 of puzzle"""
        
        # make a list of all of the small caves        
        self.small_caves = [cave for cave in self.caves if cave.islower() and cave != 'start' and cave != 'end']
        
        # the total number of paths will be the sum of those found in part1, where small caves
        # could only be used once, plus all of the paths where exactly one cave was used twice
        
        total_count = self.part1_count
        
        # for each small cave, find the paths which use that cave exactly twice
        for small_cave in self.small_caves:
            self.paths = []
            
            # this gives all paths from part1 plus all the caves that use this (small_cave) exactly twice
            path = self.follow_path('start', [], small_cave_twice=small_cave)
            
            # count just the paths that use 
            count = 0
            for path in self.paths:
                if path.count(small_cave) == 2:
                    count += 1
            print(f"{count:6d} paths found which use {small_cave} twice")
            total_count += count
            
        print(f"\n{total_count:6d} total paths found")
        
        
    # def follow_path(self, from_cave, path_so_far, small_cave_twice=None, small_cave_used_twice=False):
    def follow_path(self, from_cave, path_so_far, small_cave_twice=None):
        
        path = list(path_so_far)
        path.append(from_cave)
        # if the specified small cave has already been used twice, then remember that
        if small_cave_twice is not None:
            small_cave_used_twice = True if path.count(small_cave_twice) == 2 else False
        
        # try to extend the path through each of the caves reachable from this cave (from_cave)
        for to_cave in self.caves[from_cave]:
            # if 'end' is reachable, then record this a a possible path
            if to_cave == 'end':
                # make a copy of path before putting it into self.paths so that we can continue to 
                # modify it in this function
                terminal_path = list(path)
                terminal_path.append('end')
                self.paths.append(terminal_path)
                
            # otherwise, check to see if visiting this cave is valid    
            elif not to_cave.islower() or to_cave not in path_so_far or         \
                    (to_cave == small_cave_twice and not small_cave_used_twice):
                # we can validly visit this cave (to_cave), so continue to build the path
                self.follow_path(to_cave, path, small_cave_twice)
    
    
    #staticmethod
    def print_caves(list_of_caves):
        print('  ', end='')
        comma = ''
        for cave in list_of_caves:
            print(f"{comma}{cave}", end='')
            comma = ','
        
        
        
    def prepare_input_list(self, lines):
        """create a list of the input"""
        # create a dictionary with an entry for each cave containing a list of connections
        caves = {}
        for line in lines:
            # split the line into a list containing the two cave names
            pair = line.split('-')
            # create a list containing the two caves twice, [a,b] and [b,a]
            pairs = [pair, pair[::-1]]
            # for each order
            for a, b in pairs:
                # connection is from a to b
                # do not make a connection 'to' start
                if b != 'start':
                    if a in caves:
                        caves[a].append(b)
                    else:
                        caves[a]= [b]
        
        print(f"\nInput caves and connections\n")
        for cave, connections in caves.items():
            print(f"cave: {cave:5s}  - ", end='')    
            AdventPuzzle.print_caves(connections)
            print()
        print()    
        return caves
        
    
# import code common for all Advent puzzles
import advent 
# pass module name, and package
advent.startup(__name__, __package__, obj=True)

