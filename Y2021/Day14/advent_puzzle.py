# description required by advent.py
description = (("Determine the difference between most common and least common element in the polymer",       # part 1
                "after 10 steps"),
               ("Determine the difference between most common and least common element in the polymer",       # part 2  
                "after 40 steps")      
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
        self.prepare_input_list(lines)
        
        # create a list of counts, initialized to zeros for part2
        self.rule2_counts = [0 for _ in self.rules1]
        
        # for each pair of elements in the initial template
        # add one to the count for the element that is the
        # left side of the pair
        for pair in self.template_pairs():
            for r, rule in enumerate(self.rules1):
                if pair == rule[0]:
                    self.rule2_counts[r] += 1
        # the last element in the initial template will
        # not be counted by the method used in part 2
        # so keep track of what it is so we can add one 
        # for that element at the end
        self.last_element_in_template = self.template[-1]
        
        # convert the part1 rules list for part2
        self.rules2 = [[self.rule_index(pair[0] + insert),
                        self.rule_index(insert + pair[1]), 
                        pair]   for pair, insert in self.rules1]             
        
        # create a list of all the elements in the input data
        self.elements = []    
        # there is a rule for every possible pair of elements
        # (this is not explicit in the problem statement, but
        #  is implicit in the data) (and the method of part2 would
        #  not work if it was false)      
        
        # all elements will be found by looking at the first element
        # of each pair in the rules.  
        for rule in self.rules1:
            if rule[0][0] not in self.elements:
                self.elements.append(rule[0][0])
                


    def puzzle_part1(self):
        """run  part1 of puzzle"""
        
        templen = len(self.template)
        resultlen = (2**10 * (templen - 1)) + 1
        print(f"for a template of length {len(self.template)}, and 10 iterations, the result will be {resultlen:,d} elements")
        print()
        # part1 runs the polymer element pairing algorithm for 10 steps
        for step in range(10):
            next_template = ''
            # produce a new template by inserting elements according
            # to the rules
            for pair in self.template_pairs():
                insert = self.apply_rule1(pair)
                next_template += pair[0] + insert
            # add in the element at the end (always the same)
            next_template += pair[1]
            # update self.template from next_template
            self.template = next_template
                    
        print(f"after 10 steps")
        
        self.print_results(self.part1_element_count)


    def part1_element_count(self, element):
        """count the number of times 'element' is in the polymer"""
        return self.template.count(element)
        
    
    def puzzle_part2(self):
        """run part2 of puzzle"""
        
        templen = len(self.original_template)
        resultlen = (2**40 * (templen - 1)) + 1
        print(f"for a template of length {templen}, and 40 iterations, the result will be {resultlen:,d} elements")
        print()
        # part2 runs the polymer element pairing algorithm for 40 steps
        # we cannot use the scheme from part1 because the resulting string would be 
        # more than 20 terabytes long
        # this algorithm keeps track of how many instances of each rule exist in the
        # string (which we don't generate), and increasing and decreasing those counts for
        # each step
        steps = 40
        for step in range(steps):
            # make a copy of the counts for the rules so we can modify it as we go
            step_counts = list(self.rule2_counts)
            # for each rule (and its count) generate count * each of the pairs
            # that the rule generates and remove the count of the generating pair
            for r, (rule, count) in enumerate(zip(self.rules2, self.rule2_counts)):
                if count > 0:
                    # left is the index into the rules (and counts) for the left element plus the inserted element
                    # right is the index into the rules (and counts) for the inserted element plus the right element
                    left, right, pair = rule
                    step_counts[left] += count
                    step_counts[right] += count
                    step_counts[r] -= count
            self.rule2_counts = step_counts
            
        print(f"after {steps} steps:")
        
        self.print_results(self.part2_element_count)
            

    def part2_element_count(self, element):
        """get the count of the number of pairs in the polymer string that have this element on the left"""
        count = 0
        for r, rule in enumerate(self.rules2):
            rule_element = rule[2][0]   
            if element == rule[2][0]:
                count += self.rule2_counts[r]
        # if this is the element that appeared at the end of the original template, then it is still there
        # but not included in the above count.  Add one to include it
        if element == self.last_element_in_template:
            count += 1
        return count

    

    def print_results(self, element_count):
        """print the results using the appropriate function (supplied as a parameter) to count the elements"""
        max_count = 0
        min_count = None
        print(f" element counts:")
        
        for element in self.elements:
            count = element_count(element)
            
            print(f"  element {element}:    {count:18,d}")
            
            if count > max_count: max_count = count
            if min_count is None or count < min_count: min_count = count
            
        print(f"maximum count = {max_count:18,d}")
        print(f"minimum count = {min_count:18,d}")
        print(f"difference    = {max_count - min_count:18,d}")        




    def template_pairs(self):
        """generate all of the paris of elements from a template string"""
        for i in range(len(self.template)-1):
            yield self.template[i:i+2]
        
            
    def rule_index(self, pair):
        """get the index of a rule, given its pair of elements"""
        for i, rule in enumerate(self.rules1):
            if rule[0] == pair:
                return i

        
    def apply_rule1(self, pair):
        """find the rule for the given pair and return the triplet (if any)"""
        insert = ''
        for rule in self.rules1:
            if pair == rule[0]:
                insert = rule[1]
        return insert
        
        
    def prepare_input_list(self, lines):
        """create a list of the input"""
        self.rules1 = []
        for i, line in enumerate(lines):
            if i == 0:
                self.template = line
                self.original_template = line
            elif i > 1:
                pair, insert = line.split(' -> ')
                # new_rule = [pair, insert, 0]
                new_rule = [pair, insert]
                self.rules1.append(new_rule)

    
# import code common for all Advent puzzles
import advent 
# pass module name, and package
advent.startup(__name__, __package__, obj=True)

