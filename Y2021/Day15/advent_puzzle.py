# description required by advent.py
description = (("Find the optimal path through the cave, with the least risk",       # part 1
                "using the supplied 100x100 map.  Print the total riskx"),
               ("Find the optimal path through the cave, with the least risk",       # part 2       
                "using an expanded 500x500 map.  Print the total riskk") 
              )
              
import TimingManager as tm
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
        self.risks = self.prepare_input_list(lines)


    def puzzle_part1(self):
        """run  part1 of puzzle"""
        
        # Use Dijkstra's algorithm to find the shortest path
        self.dijkstra(source=(0,0), target=(self.size_x-1, self.size_y-1))
        

    def puzzle_part2(self):
        """run part2 of puzzle"""
        
        # expand the input to be 5 times bigger in each direction
        # the risk values for the expanded sections are derived from the original input file
        new_tile_risks = []
        for row in self.risks:
            new_row = list(row)
            prev_tile_row = list(row)
            for n in range(4):
                next_tile_row = []
                for v in prev_tile_row:
                    v += 1
                    if v > 9:
                        v = 1
                    next_tile_row.append(v)
                    new_row.append(v)
                prev_tile_row = next_tile_row
            new_tile_risks.append(new_row)
        
        new_risks = list(new_tile_risks)
        next_risks = list(new_tile_risks)
        for n in range(4):
            prev_risks = next_risks
            next_risks = []
            for row in prev_risks:
                next_tile_row = []
                for v in row:
                    v += 1
                    if v > 9:
                        v = 1
                    next_tile_row.append(v)
                new_risks.append(next_tile_row)
                next_risks.append(next_tile_row)
        
        self.risks = new_risks
        self.size_x = len(new_risks[0])
        self.size_y = len(new_risks)
        
        # compute the shortest path from source to target using Djikstra's algorithm
        self.dijkstra(source=(0,0), target=(self.size_x-1, self.size_y-1))             
        

    def dijkstra(self, source, target):
        """use Djikstra's algorithm to find the shortest path"""
                
        # unvisited is a dictionary keyed by x,y location,
        # which contains the best path found so far from source to location x,y
        unvisited = {node: 99999999 for node in [(x,y) for x in range(self.size_x) for y in range(self.size_y)]}        
        
        # have distance is like unvisited but contains only the subset of locations that are
        # candidates to be considered for the next iteration
        have_distance = {source:0}
        
        # parents will contain the immediate parent of location x,y for the optimal path from source to x,y
        parents = {}
        
        # current location whose optimal path will be found on the next iteration
        # initialized to the source location
        current = source
        current_distance = 0
        unvisited[source] = current_distance
        
        # Djikstra's algorithn for shortest path
        with tm.TimingManager('Dijkstra algorithm', elapsedOnly=True):
            while True:
                # current is the unvisited node that is closest to the source
                for neighbor, distance in self.neighbor_distances(current):   # 2,3 or 4 neighbors
                    # new_distance is distance from the source to this neighbor on this path
                    new_distance = current_distance + distance
                    # if the neighbor has no distance from the source yet or the new distance is less than previous best path
                    if new_distance < unvisited[neighbor]:
                        # update this neighbor with the new distance
                        unvisited[neighbor] = new_distance
                        have_distance[neighbor] = new_distance
                        # the current node is the shortest known path (so far) to the neighbor
                        parents[neighbor] = current
                        
                # we now have the shortest path from the source to 'current'
                # remove it from the have_distance dictionary so we won't consider it further
                del have_distance[current]
                
                # if we have the shortest path to the target then we are done
                if current == target:
                    break
                    
                # have_distance contains only those unvisited nodes for which we have computed a distance from the source
                # The node in have_distance with the shortest path from the souce will become the next 'current'
                # and in the next iteration we will have the optimal path from the source to it
                current_distance = 999999
                for node_id, distance in have_distance.items():
                    if distance < current_distance:
                        current = node_id
                        current_distance = distance
            
            # we have completed the calculation of the path from source to target
            # now backtrack through the 'parents' list from target back to source
            # to produce the optimal path, and compute the total risk of the path
            path = self.compute_path(parents, source, target)
            
            # compute the number of steps and the total risk of the optimal path
            total_risk = 0
            total_steps = 0
            for node in path:
                node_x = node[0]
                node_y = node[1]
                if node != source:
                    risk = self.risks[node_y][node_x]
                    total_risk += risk
                    total_steps += 1
                    
            # print the path (if the grid is not too big)
            self.print_path(path)
        
        print(f"total steps={total_steps}")    
        print(f"total risk={total_risk}")


    def neighbor_distances(self,loc):
        """iterate over neighbors and their distances"""
        x,y = loc
        for xp, yp in self.neighbors(x,y):
            yield (xp,yp), self.risks[yp][xp]


    def print_path(self, path):
        """print the grid with the path if it isn't too big"""
        if self.size_x > 100:
            return
        for y, row in enumerate(self.risks):
            for x, c in enumerate(row):
                if (x,y) in path:
                    bright = advent.BRIGHT
                else:
                    bright = advent.DIM
                print(f"{bright}{c}{advent.NORMAL}", end='')
            print()
        print()


    def compute_path(self, parents, source, target):
        """given the list of parents, source and target: compute the path"""
        path = []
        next_node = target
        while True:
            path.insert(0,next_node)
            if next_node == source:
                break
            next_node = parents[next_node]
        return path
    
    
    def neighbors(self, x, y):
        """generate coordinates for neighbors of location x,y """
        
        neighbors_set = ((0,-1),(-1,0),(1,0),(0,1))
        
        for dx, dy in neighbors_set:
            # compute x, y coordinates of each of the four neighbors
            xp, yp = x+dx, y+dy
            # if the neighbor is within the grid return its coordinates
            if 0 <= xp < self.size_x and 0 <= yp < self.size_y:
                yield xp, yp
        
        
    def prepare_input_list(self, lines):
        """create a list of the input"""
        self.size_y = len(lines)
        self.size_x = len(lines[0])
        
        risks = [[int(v) for v in line] for line in lines]
        
        return risks
        
    
# import code common for all Advent puzzles
import advent 
# pass module name, and package
advent.startup(__name__, __package__, obj=True)

