# description required by advent.py
description = (("Run the MONAD algorithm to validate model numbers",        # part 1
                "find the largest valid model number"),
               ("Run the MONAD algorithm to validate model numbers",        # part 2       
                "find the smallest valid model number") 
              )

"""

The MONAD program has a "stack" (done using * 26, / 26, % 26) to retrieve/add the previous input

There are 14 inputs:
    - 7 to add a digit
    - 7 more to check the digits that were added
The goal is to make sure all 7 insertions are valid

An insertion is "valid" if the difference between the last digit in the stack and
the check digit that was just input is equal to a hardcoded value

These are the hardcoded values my puzzle input had:

store w1 + 15
  store w2 + 8
    store w3 + 2
    check w4 == w3 + 2 - 9          (w4 = w3 - 7)   max: w4=2,  w3=9    min: w4=1, w3=8
    store w5 + 13
      store w6 + 4
        store w7 + 1                
        check w8 == w7 + 1 - 5      (w8 = w7 - 4)   max: w8=5,  w7=9    min: w8=1, w7=5
        store w9 + 5
        check w10 == w9 + 5 - 7     (w10 = w9 - 2)  max: w10=7, w9=9    min: w10=1, w9=3
      check w11 == w6 + 4 -12       (w11 = w6 - 8)  max: w11=1, w6=9    min: w11=1, w6=9
    check w12 == w5 + 13 - 10       (w12 = w5 + 3)  max: w12=9, w5=6    min: w12=4, w5=1
  check w13 == w2 + 8 - 1           (w13 = w2 + 7)  max: w13=9, w2=2    min: w13=8, w2=1
check w14 == w1 + 15 - 11           (w14 = w1 + 4)  max: w14=9, w1=5    min: w14=5, w1=1

The maximum solution is:
  52926995971999
  
The minimum solution is:
  11811951311485

This gives seven equations that must be satisfied for the number
defined by w1 through w14 to be valid.  

To maximize the solution, we find the largest values of w1 through
w14 that satisfy the equations.

To minimize the solution, we find the smallest values of w1 through
w14 that satisfy the equations.

All of the constants above are values found in the input 'program'

"""



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
        self.steps = self.prepare_input_list(lines)


    def puzzle_part1(self):
        """run  part1 of puzzle"""
        w = [0] * 14
        stack = []
        # process the 14 steps
        for step, (step_type, step_val) in enumerate(self.steps):
            
            if step_type == 'store':
                # this step is a store; push the value onto the stack
                indent = ' ' * (len(stack) * 2)
                print(f"{indent}store push ({step},{step_val})")
                stack.insert(0, (step, step_val))
            else:
                # this step is a check; pop the stored value from the stack
                store_step, store_val = stack.pop(0)
                indent = ' ' * (len(stack) * 2)
                print(f"{indent}check pop  ({store_step},{store_val}) with {step_val}")
                w_check = store_val + step_val
                # find the highest pair of input digits (1:9) that satisfy the equation
                if w_check > 0:
                    w[store_step] = 9 - w_check
                    w[step] = 9
                else:
                    w[step] = 9 + w_check
                    w[store_step] = 9
        print()       
        print(f"largest valid model number = {''.join([str(v) for v in w])}")
        
    
    def puzzle_part2(self):
        """run part2 of puzzle"""
        w = [0] * 14
        stack = []
        # process the 14 steps
        for step, (step_type, step_val) in enumerate(self.steps):
            
            if step_type == 'store':
                # this step is a store; push the value onto the stack
                indent = ' ' * (len(stack) * 2)
                print(f"{indent}store push ({step},{step_val})")
                stack.insert(0, (step, step_val))
            else:
                # this step is a check; pop the stored value from the stack
                store_step, store_val = stack.pop(0)
                indent = ' ' * (len(stack) * 2)
                print(f"{indent}check pop  ({store_step},{store_val}) with {step_val}")
                w_check = store_val + step_val
                # find the lowest pair of input digits (1:9) that satisfy the equation
                if w_check > 0:
                    w[store_step] = 1
                    w[step] = 1 + w_check
                else:
                    w[step] = 1
                    w[store_step] = 1 - w_check
        
        print()        
        print(f"smallest valid model number = {''.join([str(v) for v in w])}")
        
        
    def prepare_input_list(self, lines):
        """create a list of steps"""
        steps = []
        step_type = None
        step_val = None
        
        for line in lines:
            fields = [line[0:5]]
            if len(line) > 5:
                fields.append(line[5:])
            else:
                fields.append(' 0')
            cmd, val = fields
            val = val.strip()
            if cmd == 'div z':
                # the 'div z' instruction determines whether this step is a 'store' or a 'check'
                if val == '1':
                    step_type = 'store'
                else:
                    step_type = 'check'
                    
            elif cmd == 'add x' and step_type == 'check':
                # the last 'add x' defines the check constant
                step_val = int(val)
            
            elif cmd == 'add y' and val != 'w' and step_type == 'store':
                # the last 'add y' defines the value added to 'w'
                step_val = int(val)
                
            elif cmd == 'add z':
                # this is the end of the step
                steps.append((step_type, step_val))
                step_type = None
                step_val = None
        
        return steps
        
            
    
# import code common for all Advent puzzles
import advent 
# pass module name, and package
advent.startup(__name__, __package__, obj=True)

