# description required by advent.py
description = (("Find the cheapest set of moves to organize the amphipods",        # part 1
                "Each amphipod room holds two amphipods"),
               ("Find the cheapest set of moves to organize the amphipods",        # part 2       
                "Each amphipod room holds four amphipods") 
              )

from copy import deepcopy
from functools import lru_cache

# to run:
#   put advent_puzzle.py and advent.py into a folder
#   navigate to that folder
#   execute  python3 advent_puzzle.py

#   advent.py contains functions that are (will be common) to all of the puzzles
#   and advent.py and advent_puzzle.py have some complications because I have set
#   them up to be able to be executed in a batch with more puzzles.  You can ignore
#   that.  

def podx(pod):
    """convert an amphipod type ('A', 'B', etc) into an index (0, 1, etc)"""
    if pod is None:
        return 
    return ord(pod) - ord('A')

def xpod(pox):
    """convert an amphipod index (0, 1, etc) into a type ('A', 'B', etc)"""
    if xpod is None:
        return None
    return chr(pox + ord('A'))
    
class AdventPuzzle():
    def __init__(self, lines):
        """initialize the AdventPuzzle object"""
        self.rooms1, self.rooms2 = self.prepare_input_list(lines)
        self.costs = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}


    def puzzle_part1(self):
        """run  part1 of puzzle"""
        
        self.run_algorithm(self.rooms1)
        
        
    def puzzle_part2(self):
        """run part2 of puzzle"""
        
        self.run_algorithm(self.rooms2)
    
    
    def run_algorithm(self, rooms):
        """run the movement algorithm with the input state"""
        
        # initial empty state of the hallway
        hallway = (None, None, 'X', None, 'X', None, 'X', None, 'X', None, None)
           
        # system state is (hallway, rooms)
        self.find_path.cache_clear()
        ans = self.find_path((hallway, rooms))
        print(self.find_path.cache_info())
        print(f"lowest cost scheme is {ans}")
    
    
    @lru_cache(maxsize=None)    
    def find_path(self, sys):
        """find the cheapest set of moves to organise the amphipods"""
        if self.finished(sys):
            return 0
        hallway, rooms = sys
        # if any amphipod in the hallway can move home, do it right now
        for hall_idx, pod in enumerate(hallway):
            pox = podx(pod)
            if pod and pod is not 'X' and self.room_is_open(pod, rooms[pox]):
                room_idx = (pox+1)*2
                dist = self.open_path(hallway, hall_idx, room_idx)
                if dist:
                    # path to home is open
                    # find a slot in the target room and compute distance
                    slot = self.room_slot(rooms[pox])
                    dist += slot + 1
                    cost_of_this_move = self.costs[pod] * dist
                    # in order to utilize the lru_cache to short circuit
                    # the search tree (and speed up the program immensely)
                    # the inputs must be hashable, which means they cannot be
                    # mutable lists or dictionaries.  So, we have to convert
                    # back and forth between lists and tuples
                    
                    # make list copies of the hallway and rooms
                    new_hallway = list(hallway)
                    new_rooms = deepcopy(list(rooms))
                    room = list(rooms[pox])
                    
                    # update the hallway for the location just vacated by the pod that moved
                    new_hallway[hall_idx] = None 
                    
                    # update the room with the pod that just moved home
                    room[slot] = pod
                    
                    # convert the new hallway and rooms back to tuples (for the lru_cache)
                    new_rooms[pox] = tuple(room)
                    new_hallway = tuple(new_hallway)
                    new_rooms = tuple(new_rooms)
                    
                    return cost_of_this_move + self.find_path((new_hallway, new_rooms))
                    
        # find a pod to move from a room to the hallway
        # try each room (there are four) and for each of these, there may be
        # multiple possible destinations in the hallway.  Find the best of
        # these combinations
        lowest_cost = 99999999
        for room_key, room in enumerate(rooms):
            if self.room_is_open(xpod(room_key), room):
                # this room has no 'foreign' pods so no one can move out
                continue
            move_idx = self.room_top(room)
            pod = room[move_idx]
            pox = podx(pod)
            for target in range(len(hallway)):
                # can only move to empty slots
                if hallway[target] is not None:
                    continue
                room_idx = (room_key+1)*2
                dist = self.open_path(hallway, target, room_idx)
                if dist:
                    dist += move_idx + 1
                    cost_of_this_move = self.costs[pod] * dist
                    # in order to utilize the lru_cache to short circuit
                    # the search tree (and speed up the program immensely)
                    # the inputs must be hashable, which means they cannot be
                    # mutable lists or dictionaries.  So, we have to convert
                    # back and forth between lists and tuples
                    
                    # make list copies of the hallway and rooms
                    new_hallway = list(hallway)
                    new_rooms = deepcopy(list(rooms))
                    room = list(rooms[room_key])
                    
                    # update the hallway with the pod that just moved to the hallway
                    new_hallway[target] = pod
                    
                    # update the room for the location just vacated by the pod that moved
                    room[move_idx] = None
                    
                    # convert the new hallway and rooms back to tuples (for the lru_cache)
                    new_rooms[room_key] = tuple(room)
                    new_hallway = tuple(new_hallway)
                    new_rooms = tuple(new_rooms)
                    
                    lowest_cost = min(lowest_cost, cost_of_this_move + self.find_path((new_hallway, new_rooms)))
                    
        return lowest_cost            
    
    
    def open_path(self, hallway, hall_idx, room_idx):
        """determine if an unblocked path exists between a hallway position and the target room"""
        
        # determine the distance between the hall position and the entrance to the room
        if hall_idx < room_idx:
            span = range(hall_idx+1, room_idx)
            dist = room_idx - hall_idx
        else:
            span = range(room_idx+1, hall_idx)
            dist = hall_idx - room_idx
        
        # check that each location in the span contains no amphipod    
        for idx in span:
            if hallway[idx] is 'X':
                continue
            if hallway[idx] is not None:
                return None
        
        # if the path is clear, return the distance
        return dist


    def room_slot(self, room):
        """find the deepest available slot in a target room"""
        max_slot = len(room)-1
        for idx, occupant in enumerate(reversed(room)):
            if occupant is None:
                return max_slot - idx
        return None

    
    def room_top(self, room):
        """find the highest, non-empty slot in a room"""
        for idx, occupant in enumerate(room):
            if occupant is not None:
                return idx
        return None


    def room_is_open(self, key, room):
        """return True if the room is available for pods to move home"""
        for occupant in room:
            if occupant is not None and occupant != key:
                return False
        return True
        
        
    def finished(self, sys):
        """return true if all amphipods are now home"""
        hallway, rooms = sys
        for home_pox, room in enumerate(rooms):
            for occupant in room:
                if occupant != xpod(home_pox):
                    return False
        return True
    
    
    def print(self, hallway, rooms, indent=0, text=None):
        """print a representation of the current state"""
        if text:
            print(text)
        print(' '*indent, end='')
        for c in hallway:
            if c == None:
                c = '.'
            print(f"{c}", end='')
        print()
        for i in range(len(rooms[0])):
            print(' '*indent, end='')
            print("  ", end='')
            for k in range(4):
                c = rooms[k][i]
                if c == None:
                    c = '.'
                print(f"{c} ", end='')
            print()
        print()
    
        
    
    def prepare_input_list(self, lines):
        """create a list of the input"""
        rooms1 = [[], [], [], []]
        rooms2 = [[], [], [], []]
        fill_rooms = rooms1
        for line in lines:
            if line == '':
                fill_rooms = rooms2
                continue
            if line[0] == ' ':
                fill_rooms[0].append(line[3])
                fill_rooms[1].append(line[5])
                fill_rooms[2].append(line[7])
                fill_rooms[3].append(line[9])
        
        rooms1[0] = tuple(rooms1[0])
        rooms1[1] = tuple(rooms1[1])
        rooms1[2] = tuple(rooms1[2])
        rooms1[3] = tuple(rooms1[3])
        rooms1 = tuple(rooms1)  
          
        rooms2[0] = tuple(rooms2[0])
        rooms2[1] = tuple(rooms2[1])
        rooms2[2] = tuple(rooms2[2])
        rooms2[3] = tuple(rooms2[3])
        rooms2 = tuple(rooms2)    
        
        return (rooms1, rooms2)
                    


# import code common for all Advent puzzles
import advent 
# pass module name, and package
advent.startup(__name__, __package__, obj=True)

