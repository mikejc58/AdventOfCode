# description required by advent.py
description = (("calculate probe trajectories to reach a target",        # part 1
                "determine maximum height achieved by a trajectory that hits the target"),
               ("calculate probe trajectories to reach a target",        # part 2        
                "determine how many different trajectories can hit the target")
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
        self.target = self.prepare_input_list(lines)
        min_x_range = self.target[0][0]
        max_x_range = self.target[0][1]
        print(f"x_min={self.target[0][0]}, x_max={self.target[0][1]}")
        print(f"y_min={self.target[1][1]}, y_max={self.target[1][0]}")
        self.min_x_velocity = None
        self.max_x_lob_velocity = None
        self.max_x_flat_velocity = self.target[0][1]
        self.max_y_flat_velocity = self.target[1][0]
        for step in range(9999):
            distance = (step * (step + 1)) / 2
            if self.min_x_velocity is None and distance > min_x_range:
                self.min_x_velocity = step
            if distance > max_x_range:
                self.max_x_lob_velocity = step - 1
                break
        print(f"minimum x velocity to reach target area {self.min_x_velocity}")
        print(f"for a lob shot (high arcing shot)")
        print(f"   maximum x velocity to reach target area {self.max_x_lob_velocity}")
        print(f"   maximum y velocity to reach target area 0")
        print(f"for a flat shot")
        print(f"   maximum x velocity to reach target area {self.max_x_flat_velocity}")
        print(f"   maximum y velocity to reach target area {self.max_y_flat_velocity}")

        #   number of steps empirically determined to be no more than 396
        #   for this puzzle's input file
        #   for any trajectory that will hit the target (tried up to 20000)
        self.max_steps_needed = 1000
        print(f"for part1, maximum steps for trajectory will be {self.max_steps_needed}")

    def puzzle_part1(self):
        """run  part1 of puzzle"""
        
        # determine the maximum height we can achieve with a shot that hits the target
        overall_max_steps_used = 0
        overall_max_height = 0
        max_start_vy = 0
        min_start_vy = None
        for start_vx in range(self.min_x_velocity, self.max_x_lob_velocity+1):
            print(f"x velocity = {start_vx:3d}", end='')
            self.max_steps_used = 0
            total_paths = 0
            for start_vy in range(0,200):
                # try a shot with velocities start_vx and start_vy
                result = self.try_shot(start_vx, start_vy)
                # result of None means that we did not hit the target
                if result is not None:
                    # trajectory hit the target
                    positions, max_height, steps = result
                    total_paths += 1
                    # update the maximum height if we exceeded the previous maximum
                    if max_height > overall_max_height:
                        overall_max_height = max_height
                    
                    if start_vy > max_start_vy:
                        max_start_vy = start_vy
                    if min_start_vy is None:
                        min_start_vy = start_vy
            print(f"   max steps used {self.max_steps_used:5d},  paths {total_paths}")
            if self.max_steps_used > overall_max_steps_used:
                overall_max_steps_used = self.max_steps_used   
                    
        print(f"overall max height {overall_max_height}")
        print(f"max steps used {overall_max_steps_used}")
        print(f"max y velocity {max_start_vy}")
        self.part1_max_steps_used = overall_max_steps_used
        self.part1_max_y_velocity = max_start_vy
    
    def puzzle_part2(self):
        """run part2 of puzzle"""
        
        print(f"Using: (from part1)")
        print(f"   maximum steps {self.part1_max_steps_used}")
        print(f"   maximum y velocity {self.part1_max_y_velocity}")
        print()
        self.overall_max_steps_used = 0
        overall_total_paths = 0
        for start_vx in range(self.min_x_velocity, self.max_x_flat_velocity+1):
            print(f"x velocity = {start_vx:3d}", end='')
            self.max_steps_used = 0
            total_paths = 0
            for start_vy in range(self.max_y_flat_velocity, self.part1_max_y_velocity+1):
                # try a trajectory with start_vx and start_vy
                result = self.try_shot(start_vx, start_vy, steps=self.part1_max_steps_used)
                # check if successful
                if result is not None:
                    # this trajectory hit the target, count it
                    total_paths += 1
                    overall_total_paths += 1
            print(f"   max steps used {self.max_steps_used:5d},  paths {total_paths}")   
            if self.max_steps_used > self.overall_max_steps_used:
                self.overall_max_steps_used = self.max_steps_used
             
        print(f"total paths {overall_total_paths}")
        
    def try_shot(self, start_vx, start_vy, steps=None):
        """simulate a launch with initial conditions"""
        if steps is None:
            steps = self.max_steps_needed

        x = 0
        y = 0
        vx = start_vx
        vy = start_vy
        # create list of positions and velocities
        #  will be returned to caller if we hit the target
        positions = [((x,y),(vx,vy))]
        
        for step in range(steps):
            x += vx
            y += vy
            if vx > 0:
                vx -= 1
            elif vx < 0:
                vx += 1
            vy -= 1
            # add this position
            positions.append(((x,y),(vx,vy)))
            # check if we are inside the target
            if  self.target[0][0] <= x <= self.target[0][1] and \
                self.target[1][0] <= y <= self.target[1][1]:
                    # hit the target
                    # find the maximum height we achieved on this trajectory
                    max_height = 0
                    for (x_pos,y_pos), vel in positions:
                        if y_pos > max_height:
                            max_height = y_pos
                    # set the maximum steps used if we exceeded the previous maximum
                    if step+1 > self.max_steps_used:
                        self.max_steps_used = step+1
                        
                    return (positions, max_height, step+1)
            
            # check if we are now below the target
            #  if we are there is no point in doing any more, this trajectory
            #  has failed            
            if y < self.target[1][0]:
                return None
        
        
    def prepare_input_list(self, lines):
        """create a list of the input"""
        xpart, ypart = lines[0][13:].split(', ')
        xpart = tuple(int(x) for x in xpart[2:].split('..'))
        ypart = tuple(int(y) for y in ypart[2:].split('..'))
        target = (xpart, ypart)
        print(f"target is {target}")
        return target
        
    
# import code common for all Advent puzzles
import advent 
# pass module name, and package
advent.startup(__name__, __package__, obj=True)

