# description required by advent.py
description = (("Play bingo with a squid",                          # part 1
                "Pick the board which will win to beat the squid"),
               ("Let the giant squid win!",                         # part 2    
                "Pick the board which will come in last, to lose")    
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
    """run part1 of puzzle"""
    
    play_bingo(lines, return_first_win=True)
    
    
def puzzle_part2(lines):
    """run  part2 of puzzle"""
    
    play_bingo(lines, return_first_win=False)


def play_bingo(lines, return_first_win):
    """play the bingo game"""
    numbers_strs = lines.pop(0).rstrip().split(',')
    drawn_numbers = [int(n) for n in numbers_strs]
    
    boards = get_boards(lines)
    # number of boards that haven't won yet
    boards_left = 1 if return_first_win else len(boards)

    winning_board = None
    # draw the numbers until we find the winner
    for number in drawn_numbers:
        for n, board in enumerate(boards):
            # apply the drawn number to each board (board may be None which will always return False)
            if apply_number_to_board(number, board):
                # if the board included the drawn number, check if it is a winner
                if is_winner(board):
                    if boards_left == 1:
                        # this is the last board to win
                        winning_board = n
                        print(f"We have the winner!  -- board number {n}")
                        print_board(board)
                        print_score(board, number)
                        break
                    else:
                        # this is not the last winner, just remove the board from the list and 
                        # continue
                        boards[n] = None
                        boards_left -= 1
                        
        if winning_board is not None:
            break    

    
def print_score(board, number):
    """print the final score"""
    sum_unmarked = 0
    # add up all the 'unmarked' squares
    for line in board:
        for val in line:
            if val < 100:
                sum_unmarked += val
    print(f"sum of unmarked squares = {sum_unmarked}")
    print(f"winning number          = {number}")
    score = sum_unmarked * number
    print(f"score = {score}")


def is_winner(board):
    """check if this board has won"""
    
    # get the row and column size
    row_col_max = len(board[0])
    # list of sums for the columns
    col_sums = [0] * row_col_max
    for row in board:
        row_sum = 0
        for col, val in enumerate(row):
            # for each marked square, increase the row and column counts and 
            # see if the row or column is completely marked, indicating a winner
            if val >= 100:
                row_sum += 1
                col_sums[col] += 1
                if row_sum == row_col_max or col_sums[col] == row_col_max:
                    # this board is a winner
                    return True
    return False


def apply_number_to_board(number, board):
    """apply the drawn number to a board"""
    if board is not None:
        for l, line in enumerate(board):
            for v, val in enumerate(line):
                if val == number:
                    # mark the square by adding 100 to the square
                    board[l][v] = val + 100
                    # this board had the drawn number, and thus has changed
                    return True
    # this board did not have the drawn number
    return False    


def get_boards(lines):
    """get the boards from the input lines"""
    
    # remove initial blank line
    lines.pop(0)
    
    boards = []
    while True:
        # get the next board (if any)
        board = new_board(lines)
        if not board:
            # if there are no more boards, exit the loop
            break
        boards.append(board)
    
    # return the list of boards    
    return boards


def new_board(lines):
    """get the next board from the input lines"""
    board = []
    while len(lines) > 0:
        line = lines.pop(0)
        if not line:
            # break when we find the blank line at the end of a board
            break
        # convert the line into a list of integers
        line = [int(n) for n in line.split()]
        # and add it to the board's lines
        board.append(line)
    return board


# ANSI control codes for highlighting marked and unmarked squares 
NORMAL = '\x1b[0m'  # for everything except the board's squares
BRIGHT = '\x1b[1m'  # for 'marked' squares
DIM =    '\x1b[2m'  # for 'unmarked' squares


def print_board(board):
    """print a board"""
    for line in board:
        for val in line:
            if val >= 100:
                # square is 'marked'
                # recover the actual value of the square
                val -= 100
                style = BRIGHT  
            else:
                # square is 'unmarked'
                style = DIM
                
            print(style + f"{val:3d}" + NORMAL, end='')
        # print to end the line of values
        print()
    # print blank line after board
    print()


# import code common for all Advent puzzles
import advent 
# pass module name, and package
advent.startup(__name__, __package__)

