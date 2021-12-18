# description required by advent.py
description = ("Count how many times digits 1, 4, 7, and 8 appear in the output digits",       # part 1
               "Decode the scrambled signals and get the 4-digit values, sum them"             # part 2        
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
    
    # create a list of all of the output digits
    outputs = []
    for line in lines:
        outputs += line.split('|')[1].split()
    
    # create sum of outputs for each output length (length is the number of signals in each digit)
    segments = [0]*8    
    for digit in outputs:
        segments[len(digit)] += 1
    
    # get the counts for lengths 2, 3, 4 and 7 (for digits '0', '7', '4', and '8')        
    unique_counts = segments[2] + segments[4] + segments[3] + segments[7]
    
    print(f"count of outputs for 1, 4, 7, and 8  is  {unique_counts}")
    
    
def puzzle_part2(lines):
    """run part2 of puzzle"""
    
    overall_sum = 0
    
    # each input line contains ten unique values that show the scrambled signals and the scrambled output digits
    for line in lines:
        # separate the signals and the outputs
        line_signals, line_outputs = line.split('|')
        # get the 4 output digits for this line
        digits = line_outputs.split()
        # get the 10 scrambled signal sets for this line and sort them into order by number of characters
        # this sort is required because we need to see the length 2 and length 4 signals
        # before we see the length 5 and 6 signals in the processing below
        signals = sorted(line_signals.split(), key=len)
        
        # sort the individual signal and digit strings into alphabetical order
        # These sorts are done so that we can compare digits and signals.  In the input file the order of
        # the signal and digit (letter codes) are randomized
        for i, digit in enumerate(digits):
            digits[i] = ''.join(sorted(digit))
        for i, signal in enumerate(signals):
            signals[i] = ''.join(sorted(signal))
            
        # setup a list that will contain the signal code for each digit 0 through 9        
        codes = [''] * 10
    
    #  segment numbering for the 7-segment displays
    
    #    0000  
    #   3    5
    #   3    5  
    #    1111  
    #   4    6 
    #   4    6 
    #    2222  
    
        # list of signal (letter codes) values for segments 5 and 6
        signal_56 = []
        # list of signal (letter codes) values for segments 1 and 3
        signal_13 = []
        
        # process the ten scrambled signal codes
        for signal_string in signals:
            if len(signal_string) == 2:
                # must be digit '1', which only has segments 5 and 6
                codes[1] = signal_string
                # create the signal_56 list which will be used to distinguish many of the other signals
                for signal in signal_string:
                    signal_56.append(signal)
                    
            elif len(signal_string) == 3:
                # must be a '7'
                codes[7] = signal_string
                
            elif len(signal_string) == 4:
                # must be a '4', which only has segments 1, 3, 5 and 6
                codes[4] = signal_string
                # create the signal_13 list which will be used to distinguish many of the other signals
                for signal in signal_string:
                    if signal not in signal_56:
                        # this signal must be for segment 1 or 3
                        signal_13.append(signal)
                        
            elif len(signal_string) == 5:
                # must be '2', '3', or '5'
                if signal_56[0] in signal_string and signal_56[1] in signal_string:
                    # must be '3'
                    codes[3] = signal_string
                    
                elif signal_13[0] in signal_string and signal_13[1] in signal_string:
                    # must be '5'
                    codes[5] = signal_string
                    
                else:
                    # must be '2'
                    codes[2] = signal_string
                    
            elif len(signal_string) == 6:
                # must be '0', '6', or '9'  
                if signal_56[0] in signal_string and signal_56[1] in signal_string:
                    # must be '0' or '9'   
                    if signal_13[0] in signal_string and signal_13[1] in signal_string:
                        # must be '9'
                        codes[9] = signal_string
                        
                    else:
                        # must be '0'
                        codes[0] = signal_string
                        
                else:
                    # must be '6'
                    codes[6] = signal_string
                    
            elif len(signal_string) == 7:
                # must be '8'
                codes[8] = signal_string
                        
        # compute the 4-digit display value
        val = 0
        for digit in digits:
            val = (val * 10) + codes.index(digit)
        
        # add the sum for this line to the overall sum
        overall_sum += val
        
    print(f"overall sum = {overall_sum}")
        
def prepare_input_list(lines):
    return list(lines)
    
# import code common for all Advent puzzles
import advent 
# pass module name, and package
advent.startup(__name__, __package__)

