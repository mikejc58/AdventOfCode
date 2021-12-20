# description required by advent.py
description = (("Enhance the image two times",        # part 1
                "Count the number of pixels now lit"),
               ("Enhance the image fifty times",        # part 2       
                "Count the number of pixels now lit") 
              )

# to run:
#   put advent_puzzle.py and advent.py into a folder
#   navigate to that folder
#   execute  python3 advent_puzzle.py

#   advent.py contains functions that are (will be common) to all of the puzzles
#   and advent.py and advent_puzzle.py have some complications because I have set
#   them up to be able to be executed in a batch with more puzzles.  You can ignore
#   that.  

to_binary_trans_table = str.maketrans('.#', '01')
from_binary_trans_table = str.maketrans('01', '.#')

def to_binary(line):
    """translate '.' and '#' to '0' and '1' """
    return line.translate(to_binary_trans_table)
    
def from_binary(line):
    """translate '0' and '1' to '.' and '#' """
    return line.translate(from_binary_trans_table)

class AdventPuzzle():
    def __init__(self, lines):
        """initialize the AdventPuzzle object"""
        self.lines = lines

    def puzzle_part1(self):
        """run  part1 of puzzle"""
        self.prepare_input_list(self.lines)
        self.run_enhance(2)
    
    def puzzle_part2(self):
        """run part2 of puzzle"""
        self.prepare_input_list(self.lines)
        self.run_enhance(50)

    def run_enhance(self, cycles):
        """run the image enhancement algorithm for the number of cycles requested"""
        # enlarge the image with '.' the first time
        # because of the infinity effects, the edges will alternate all '0's and all '1's
        self.enlarge(1, first=True)
        for k in range(cycles):
            # enlarge the image at the edges, duplicating the current edge
            self.enlarge(1)
            # apply the enhancement algorithm to the image
            self.enhance()
            # remove the edges to get rid of the infinity effects
            self.chop_edges(1)
            # re-enlarge to recover its size
            self.enlarge(1)
        
        self.print_image()
        print(f"after {cycles} cycles, {self.count_pixels()} pixels are lit")

    def count_pixels(self):
        """count the number of pixels 'lit' in the image"""
        count = 0
        for line in self.image:
            for c in line:
                if c == '1':
                    count += 1
        return count
        
        
    def enlarge(self, amount=1, first=False):
        """enlarge the image by adding to the top, bottom and sides"""
        if first:
            char_to_add = '0'
        else:
            # the character at 0,0 actually appears on all four edges
            char_to_add = self.image[0][0]
            
        for i in range(amount):
            line_len = len(self.image[0])
            top_bottom = char_to_add * line_len
            new_image = list(self.image)
            # add top and bottom rows to the image
            new_image.insert(0,top_bottom)
            new_image.append(top_bottom)
            # expand all rows on left and right
            self.image = [''.join((char_to_add, line, char_to_add)) for line in new_image]


    def chop_edges(self, amount=1):
        """remove the edges"""
        image = self.image[amount:-amount]
        self.image = [line[amount:-amount] for line in image]
            
    
    neighbors = ((-1,-1), ( 0,-1), (+1,-1), 
                 (-1, 0), ( 0, 0), (+1, 0),
                 (-1,+1), ( 0,+1), (+1,+1))
                 
    def gen_image_line(self):
        """generate an image line by applying the enhancement algorithm"""
        len_x = len(self.image[0])
        len_y = len(self.image)
        for y, line in enumerate(self.image):
            new_line = []
            for x in range(len_x):
                v = 0
                for dx, dy in AdventPuzzle.neighbors:
                    v *= 2
                    xp = x+dx
                    yp = y+dy
                    if 0 <= xp < len_x and 0 <= yp < len_y:
                        i = int(self.image[yp][xp])
                    else:
                        i = 0
                    v += i
                # v now has index into enhancement algorithm string
                c = self.image_enhance_table[v]
                new_line.append(c) 
            yield ''.join(new_line)
    
    def enhance(self):
        """enhance the image by applying the enhancement algorithm to the image"""
        self.image = [line for line in self.gen_image_line()]
        
            
    def print_image(self, image=None, raw=False):
        """print the current image"""
        # return
        if image is None:
            image = self.image
        for line in image:
            if raw:
                print(line)
            else:
                print(from_binary(line))
        print()
                

        
    def prepare_input_list(self, lines):
        """create a list of the input"""
        # first line is the image enhancement algorithm
        self.lines = lines
        lines = list(lines)
        self.image_enhance_table = to_binary(lines.pop(0))
        # remove the blank line
        lines.pop(0)
        # now get the image
        self.image = [to_binary(line) for line in lines]
        
    
# import code common for all Advent puzzles
import advent 
# pass module name, and package
advent.startup(__name__, __package__, obj=True)

