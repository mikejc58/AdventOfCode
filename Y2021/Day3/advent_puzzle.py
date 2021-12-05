# description required by advent.py
description = ("Calculate submarine power consumption",       # part 1
               "Calculate submarine life support rating"      # part 2        
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

    report = prepare_input_list(lines)

    # get the number of bits in each line
    num_bits = len(report[0])
    
    # setup a list to count one bits for each column in the lines
    ones = [0] * num_bits

    # gamma will be a line which contains the bits that are the most common 
    # in each column of the input
    gamma = []
    for bit_num in range(num_bits):
        # for each column, find the most common bit
        bit = find_common_bit(report, bit_num, 'most common', tie_goes_to=None)
        if bit is None:
            # there were an equal number of ones and zeros
            print(f"ambiguous result for bit number {bit_num}")
            return
        gamma.append(bit)

    gamma_string = ''.join(gamma)
    gamma_decimal = int(gamma_string, 2)
    print(f"gamma    {gamma_string}   {gamma_decimal:9d}")
    
    # epsilon is just the inverse of the bits in gamma
    epsilon = ['1' if bit == '0' else '0' for bit in gamma]
    
    epsilon_string = ''.join(epsilon)
    epsilon_decimal = int(epsilon_string, 2)
    print(f"epsilon  {epsilon_string}   {epsilon_decimal:9d}")
    
    power_consumption = gamma_decimal * epsilon_decimal
    print(f"power_consumption       {power_consumption:9d}")

    
def puzzle_part2(lines):
    """run part2 of puzzle"""
    
    report = prepare_input_list(lines)

    # get the number of bits in each line
    num_bits = len(report[0])
    
    oxygen_rating = get_rating(report, num_bits, 'most common')
    print(f"oxygen generator rating {oxygen_rating:9d}")
        
    co2_rating = get_rating(report, num_bits, 'least common')
    print(f"co2 scrubber rating     {co2_rating:9d}")
    
    life_support_rating = oxygen_rating * co2_rating
    print(f"life support rating     {life_support_rating:9d}")


def prepare_input_list(lines):
    # convert each line to a list of characters (which are binary bits)
    return [list(line) for line in lines]
    

def get_rating(report, num_bits, which):
    """calculate rating based on either least or most common bits"""
    # set 'tie_goes_to' based on whether we are finding 'most' or 'least' common bit
    tie_goes_to = '1' if which == 'most common' else '0'
    
    # for each bit position (starting on the left) in the report lines
    # remove the lines which don't match the 'most common' or 'least common' criteria
    for bit_position in range(num_bits):
        # we will build a new report list with only the lines that meet the criteria
        next_report = []
        common_bit = find_common_bit(report, bit_position, which, tie_goes_to)
        # include only those lines that meet the criteria in the new list
        for bit_line in report:
            if bit_line[bit_position] == common_bit:
                next_report.append(bit_line)
        # set up for testing the next bit_position
        report = next_report
        # when there is only one line left in the report we are done
        if len(report) == 1:
            break
    # convert the final report line to a binary string 
    rating_string = ''.join(report[0])
    # convert the binary string to an integer using base-2 conversion
    rating_decimal = int(rating_string, 2)
    
    return rating_decimal
            
def find_common_bit(report, bit_position, which, tie_goes_to):
    """find the most or least common bit in the given bit position"""
    report_line_count = len(report)
    ones = 0
    # look at each of the lines in the report and find the number of one bits
    # in the given bit position
    for bit_line in report:
        if bit_line[bit_position] == '1':
            ones += 1
    zeros = report_line_count - ones
    # based on whether we are finding the 'most common' or 'least common' bit in this position
    # return the result.  If the number of ones equals the number of zeros, return the
    # 'tie_goes_to' value
    if ones > zeros:
        result = '1' if which == 'most common' else '0'
    elif zeros > ones:
        result = '0' if which == 'most common' else '1'
    else:
        result = tie_goes_to
    return result
    
# import code common for all Advent puzzles
import advent 
# pass module name, and package
advent.startup(__name__, __package__)

