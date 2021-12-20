# description required by advent.py
description = (("Snailfish math homework",       # part 1
                "add up the input 'numbers' using snailfish rules"),
               ("Snailfish math homework",       # part 2  
                "find the two 'numbers' in the input that give the largest magnitude when added")    
              )

# to run:
#   put advent_puzzle.py and advent.py into a folder
#   navigate to that folder
#   execute  python3 advent_puzzle.py

#   advent.py contains functions that are (will be common) to all of the puzzles
#   and advent.py and advent_puzzle.py have some complications because I have set
#   them up to be able to be executed in a batch with more puzzles.  You can ignore
#   that.  

# class ParseError(Exception):
    # pass

class AdventPuzzle():

    class ParseError(Exception):
        pass

    def __init__(self, lines):
        """initialize the AdventPuzzle object"""
        self.grid = self.prepare_input_list(lines)


    def puzzle_part1(self):
        """run  part1 of puzzle"""
        lines = list(self.lines)
        result = lines.pop(0)
        # create the sum of all the snailfish numbers in the input
        for line in lines:
            # add the next snailfish number to the current total
            self.full_line = '[' + result + ',' + line +']'
            # perform the reduction operation after the addition
            result = self.reduce(self.full_line)
        
        # compute the 'magnitude' of the sum    
        mag = self.magnitude((result,0), 0)
        print(f" magnitude = {mag}")
        
    
    def puzzle_part2(self):
        """run part2 of puzzle"""
        # for every pair of numbers (in both orders)
        # find the pair that sum to the highest magnitude
        biggest = 0
        for left_line in self.lines:
            for right_line in self.lines:
                # the two numbers cannot be the same number twice
                if left_line is not right_line:
                    result = left_line
                    self.full_line = '[' + result + ',' + right_line + ']'
                    result = self.reduce(self.full_line)
                    mag = self.magnitude((result,0), 0)
                    if mag > biggest:
                        biggest = mag
                        biggest_left = left_line
                        biggest_right = right_line
                        
        print(f"  {biggest_left}")
        print(f"+ {biggest_right}")
        print(f" magnitude = {biggest}")


    def parse(self, line, depth):
        """parse a snailfish number into the left and right parts of the outermost pair"""
        line, position = line
        depth += 1
        position += 1
        left_bracket = line[0]
        right_bracket = line[-1]
        if left_bracket != '[' or right_bracket != ']':
            raise AdventPuzzle.ParseError("Missing left or right bracket -- " + line)
        # strip the starting and ending brackets to expose the pair
        line = line[1:-1]
        
        # it is a simple pair if all that is left is 'n,m'
        simple_pair = False if line[0] == '[' or line[-1] == ']' else True
                    
        # find left and right of pair (the comma between them is at level 0)
        level = 0
        for i in range(len(line)):
            c = line[i]
            if c == ',' and level == 0:
                break
            if c == '[':
                level += 1
            elif c == ']':
                level -= 1
        else:
            # ill formed line, with no comma at level 0
            raise AdventPuzzle.ParseError("No comma at level 0 - " + line)
            
        left = line[:i]
        right = line[i+1:]
        
        return (left,position), (right,position+i+1), simple_pair, depth


    def do_explode(self, left, right):
        """'explode the deeply nested (level=4 or more) to reduce nesting'"""
        # the line has been divided into left and right parts
        # left is a tuple with a string containing the left number of the pair and an integer 
        # which is the position in the original line of the first digit of the number
        # right is a tuple with a string containing the right number of the pair and an integer
        # which is the position in the original line of the second digit of the number
        
        left_val = int(left[0])
        right_val = int(right[0])
        
        pair_left_position = left[1]-1
        pair_right_position = right[1]+1
        while self.full_line[pair_right_position] != ']':
            pair_right_position += 1
            
        # split the original line into two parts, omitting the pair
        left_part = self.full_line[:pair_left_position]
        right_part = self.full_line[pair_right_position+1:]
        
        # find the number to the left which will get the left value added to it
        
        # first search for the last digit of that number
        for i in range(len(left_part)-1, -1, -1):
            if left_part[i].isdigit():
            
                # now scan for the first digit of that number
                for j in range(i, -1, -1):
                    if not left_part[j].isdigit():
                        val = int(left_part[j+1:i+1])
                        
                        # now add the left parm to the val
                        # split the left part itself into two parts
                        val_left_part = left_part[:j+1]
                        val_right_part = left_part[i+1:]
                        
                        # update the number 
                        left_part = val_left_part + f"{val+left_val}" + val_right_part
                        # we are done with the left part
                        break
                else:
                    # there should be at least one '[' to the left of the number
                    raise AdventPuzzle.ParseError("Missing left bracket -- " + left_part)
                break
        else:
            # no previous number found
            # in that case the left value of the pair is discarded
            pass
        
        # insert the required '0' to replace the pair    
        left_part = left_part + '0'    
        
        # now we process the right number of the pair in a similar way
        
        # scan for the start of the next numeric value
        for i in range(0,len(right_part)):
            if right_part[i].isdigit():
                # now scan for the end of the next numeric value
                for j in range(i,len(right_part)):
                    if not right_part[j].isdigit():
                        val = int(right_part[i:j])
                        
                        # now add the right parm to the val
                        # split the right part itself into two parts
                        val_left_part = right_part[:i]
                        val_right_part = right_part[j:]
                        
                        # update the number
                        right_part = val_left_part + f"{val+right_val}" + val_right_part
                        # we are done with the right part
                        break
                else:
                    # there should be at least one ']' to the right of the number
                    raise AdventPuzzle.ParseError("Missing right bracket -- " + right_part)
                break
        else:
            # no next number found
            # in that case the right value of the pair is discarded
            pass
            
        # join the left and right parts to recreate the line
        line = left_part + right_part
        
        return (True, line)


    def magnitude(self, line, depth):
        """recursively compute the 'magnitude' of a snailfish number"""
        left, right, simple_pair, depth = self.parse(line, depth)
        
        left_val =  self.magnitude(left, depth)  if left[0][0]  is '[' else int(left[0])
        right_val = self.magnitude(right, depth) if right[0][0] is '[' else int(right[0])
                    
        return (left_val * 3) + (right_val * 2)
        

    def explode(self, line, depth):
        """recursively scan for a pair that needs to be exploded"""
        left, right, simple_pair, depth = self.parse(line, depth)
        done = False
        if simple_pair:
            if depth > 4:
                # found a pair that must be exploded (done will be set to True)
                done, line = self.do_explode(left, right)
        else:
            if not done and left[0][0] == '[':
                done, line = self.explode(left, depth)
            if not done and right[0][0] == '[':
                done, line = self.explode(right, depth)
                
        if done == False:
            line = self.full_line
            
        return (done, line)


    def split(self, line):
        """split any value in the snailfish number which is greater than 9 (two or more digits)"""
        for i in range(len(line)):
            # scan for a numeric digit
            if line[i].isdigit():
                # found start of number
                for j in range(i+1, len(line)):
                    if not line[j].isdigit():
                        if j > i+1:
                            # is multiple digits
                            val = int(line[i:j])
                            left_part = line[:i]
                            right_part = line[j:]
                            half_val = int(val/2)
                            line = left_part + f"[{half_val},{half_val + val%2}]" + right_part
                            return (True, line)
                        break
                else:
                    # failed to find end of number
                    raise AdventPuzzle.ParseError("Missing right bracket -- " + line)

        return (False, line)

    
    def reduce(self, line):
        """iteratively explode and split snailfish numbers until there is no more that can be done"""
        retval = True
        while retval:
            self.full_line = line
            retval, line = self.explode((line,0), 0)
            if not retval:
                retval, line = self.split(line)
        return line
            
    
        
    def prepare_input_list(self, lines):
        """create a list of the input"""
        self.lines = lines
    
# import code common for all Advent puzzles
import advent 
# pass module name, and package
advent.startup(__name__, __package__, obj=True)

