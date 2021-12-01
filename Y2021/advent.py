
import sys
import os

def startup(my_name, my_package):
    if my_package == None:
        my_file_prefix = ''
    else:
        my_file_prefix = my_package+'/'
    # called by each advent_puzzle.py when loaded
    if my_name == '__main__':
        # with advent.py in .../Y2021/ and advent_puzzle.py in .../Y2021/Day1/
        #   advent_puzzle.py invoked via:  .../Y2021 > python3 -m Day1.advent_puzzle [filename]
        #   (note: -m and the name  Day1.advent_puzzle  NOT  Day1/advent_puzzle.py)
        #   the input file can be specified on the command line, and must be in .../2021/Day1
        #   or, if not specified, 'input.txt' will be looked for in .../Y2021/Day1
        #   if 'input.txt' is not found then it will look for 'sample.txt'
        #   (note) the actual directory names are not important, but the structure is
        #          so the above could be .../mydir1/mydir2/ instead of .../Y2021/Day1
        #          EXCEPT, this won't work if one of the directories starts with a digit
        #                  (some sort of python crazyness)
        # alternatively:
        
        # with advent.py and advent_puzzle.py in the same directory .../mydir/
        #   advent_puzzle.py invoked via:  .../mydir > python3 advent_puzzle.py [filename]
        #   the input file can be specified on the command line, and must be in .../mydir/ 
        #   or, if not specified, 'input.txt' will be looked for in .../mydir/
        #   if 'input.txt' is not found then it will look for 'sample.txt'
        
        input_file = None
        # if filename specified on the command line
        if len(sys.argv) > 1:
            input_file = my_file_prefix+sys.argv[1]
            
        # otherwise use 'input.txt' if it exists, if not try 'sample.txt'
        else:
            input_txt = my_file_prefix+'input.txt'
            sample_txt = my_file_prefix+'sample.txt'
            
            if os.path.isfile(input_txt):
                input_file = input_txt
                
            elif os.path.isfile(sample_txt):
                input_file = sample_txt
                
        if input_file is None:
            print("No input file found")
            exit()
        
        # run the part1 and part2 puzzle code
        sys.modules[my_name].puzzle(input_file, part='both')
        
    else:
        # advent_puzzle was imported into test_all.py
        # test_all.py imports multiple advent_puzzle files (perhaps from multiple days)
        # and runs them all
        
        # test_all.py invoked via:  .../2021 > python3 -m Day1.advent_puzzle
        # (note: -m and the name ... Day1.advent_puzzle  NOT  Day1/advent_puzzle.py)
    
        main = sys.modules['__main__']          # get a reference to the test driver module
        myself = sys.modules[my_name]           # get a reference to this module
        main.mod_list.append([myself, my_package])  # add myself to the list of modules to be tested
        
        
# functions common to all puzzles
def read_input(file_name, prep_function=None):
    """read the input lines into a list"""
    lines = []
    with open(file_name) as input_file:
        for line in input_file:
            line = line.rstrip()
            if prep_function:
                line = prep_function(line)
            lines.append(line)
    return lines



