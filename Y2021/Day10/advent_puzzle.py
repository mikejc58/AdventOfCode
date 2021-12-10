# description required by advent.py
description = (("Find corrupt lines and, for each, compute a syntax error score",    # part 1
                "Compute the total syntax error score for the file"),
               ("Find incomplete lines and, for each, compute a autocomplete score", # part 2  
                "Find the median autocomplete score for the file")     
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
        self.lines = self.prepare_input_list(lines)
        self.closings = {'(':')', '[':']', '{':'}', '<':'>'}
        self.illegal_scores = {')': 3, ']': 57, '}': 1197, '>': 25137}
        self.complete_points = {')': 1, ']': 2, '}': 3, '>': 4}
        self.print_lines = True if len(lines) < 20 else False


    def puzzle_part1(self):
        """run  part1 of puzzle"""
        
        # find the corrupt lines and compute a total 'syntax error' score for the file
        syntax_error_score = 0
        for line_no, line in enumerate(self.lines):
            syntax_error_score += self.score_corrupt_line(line, line_no)
            
        print(f"Syntax Error Score {syntax_error_score}")
    
    
    def puzzle_part2(self):
        """run part2 of puzzle"""
        autocomplete_points = []
        for line_no, line in enumerate(self.lines):
            points = self.auto_complete_line(line, line_no)
            if points:
                autocomplete_points.append(points)
        
        # find the median of the points returned for each line
        #  (we are guaranteed by the puzzle definition that there will be an odd number of incomplete lines)        
        autocomplete_points.sort()
        median = int(len(autocomplete_points)/2)
        
        print(f"median index={median}, median value={autocomplete_points[median]}")
        
    def prepare_input_list(self, lines):
        """create a list of the input"""
        return lines

    def parse_line(self, line):
        """parse the line and determine if it is corrupted or merely incomplete"""
        
        # stack to contain expected closing characters
        stack = []
        
        # scan the line for opening and closing characters
        for char_no, c in enumerate(line):
            if c in '([{<':
                # for opening characters ([{<
                # stack the expected closing character
                stack.append(self.closings[c])
            else:
                # is closing characters )]}>
                # pop the expected closing character from the stack
                required_closing = stack.pop()
                # if the closing character does not match, the line is corrupt
                if c != required_closing:
                    return ('corrupt', (char_no, c, required_closing))
        
        # if there are still expected closing characters on the stack
        # then the line is incomplete
        if len(stack) != 0:
            return ('incomplete', (stack,))
            
        # if the stack is empty, then this line is valid
        #  (this should never happen in this puzzle)
        else:
            return ('valid', (None,))
        

    def score_corrupt_line(self, line, line_no):
        """find corrupted lines and return a syntax error score for them"""
        
        # parse the line
        result, result_data = self.parse_line(line)
        
        if result == 'corrupt':
            # return the 'score' for this corrupt line
            char_no, c, required_closing = result_data
            score = self.illegal_scores[c]
            if self.print_lines:
                print(f"line: {line_no:3d}, character: {char_no:3d} -- expected {required_closing}, but found {c}")
                print(f"  score  = {score}")
            return score
            
        elif result == 'valid':
            print(f"*** Unexpected valid line ***  {line}")
            
        return 0
        
        
    def auto_complete_line(self, line, line_no):
        """find incomplete lines and return an autocomplete score for them"""
        result, result_data = self.parse_line(line)
        if result == 'incomplete':
            # return the 'score' for this incomplete line
            stack, = result_data
            
            if self.print_lines:
                print(f"line: {line_no:3d}, required closing: ", end='')
                
            score = 0
            for c in reversed(stack):
                
                if self.print_lines:
                    print(f"{c}", end='')
    
                score *= 5
                score += self.complete_points[c]
                
            if self.print_lines:
                print(f"\n  points = {score}")
                
            return score
            
        elif result == 'valid':
            print(f"*** Unexpected valid line ***  {line}")
                
        return None
                
    
# import code common for all Advent puzzles
import advent 
# pass module name, and package
advent.startup(__name__, __package__, obj=True)

