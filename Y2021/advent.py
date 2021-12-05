
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
        # sys.modules[my_name].puzzle(input_file, part='both')
        puzzle(input_file, part='both')
        
    else:
        # advent_puzzle was imported into test_all.py
        # test_all.py imports multiple advent_puzzle files (perhaps from multiple days)
        # and runs them all
        
        # test_all.py invoked via:  .../2021 > python3 -m Day1.advent_puzzle
        # (note: -m and the name ... Day1.advent_puzzle  NOT  Day1/advent_puzzle.py)
    
        main = sys.modules['__main__']          # get a reference to the test driver module
        myself = sys.modules[my_name]           # get a reference to this module
        main.mod_list.append([myself, my_package])  # add myself to the list of modules to be tested


def puzzle(input_file, part='both'):
    """run part1 and part2 of the puzzle
         parameters are the input file name, and a parameter that
         can be 1 to execute only Part1, 2 to execute only Part2 or 'both' to execute both parts
    """
    main = sys.modules['__main__']
    
    # read the input lines, convert them to integers and put them in a list of lines
    lines = read_input(input_file)
    
    if part != 'both':
        print('-'*80)
    print(f"{len(lines)} Lines read from {input_file}")
    print('-'*80)
    
    if part == 1 or part == 'both':
        print(f"\nPart 1 - {main.description[0]}")
        sys.modules['__main__'].puzzle_part1(list(lines))
        
    if part == 'both':
        print('-'*80)
    
    if part == 2 or part == 'both':
        print(f"\nPart 2 - {main.description[1]}")
        sys.modules['__main__'].puzzle_part2(list(lines))
        
        
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

def split__command_number(line):
    """split a line into a list with a command (str) and a number (int)"""
    line = line.split()
    line[1] = int(line[1])
    return line

def split__characters(line):
    """split a line into a list of single characters"""
    return list(line)

def split__words(line):
    """split a line into a list of words, removing punctuation"""
    line = [word.rstrip(',;:.? ') for word in line.split()]
    return line
