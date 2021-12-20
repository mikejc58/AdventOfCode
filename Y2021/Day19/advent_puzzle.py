# description required by advent.py
description = (("Find which beacons are seen by multiple scanners",                    # part 1
                "and determine how many unique beacons exist"),
               ("Find the location and orientation of each scanner and beacon",        # part 2    
                "determine the largest 'manhattan' distance between any two scanners")    
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
        self.lines = self.prepare_input_list(lines)
        self.scanners = [scanner for scanner in Scanner.generator(self.lines)]
        self.beacons = {}
        
        # the first step here is to identify beacons which are observed by multiple scanners
        # and to assign a unique beacon id so that all scanners will see them as the same beacons
        for ixa, scanner_a in enumerate(self.scanners):
            for ixb, scanner_b in enumerate(self.scanners[ixa+1:], ixa+1):
                for (i_aa, beacon_aa), (i_ab, beacon_ab) in scanner_a.beacon_pairs():
                    # for each pair of beacons in two scanners, compute the distance
                    # between them (as seen by each of the scanners). if the two computed
                    # distances are the same, then the pairs represent the same two beacons
                    # we still have to identify which of each pair corresponds to which of the other pair
                    distance_a = Beacon.distance_squared(beacon_aa, beacon_ab)
                    for (i_ba, beacon_ba), (i_bb, beacon_bb) in scanner_b.beacon_pairs():
                        distance_b = Beacon.distance_squared(beacon_ba, beacon_bb)
                        if distance_a == distance_b:
                            scanner_a.beacons[i_aa].add_possible_matches((i_ba, i_bb))
                            scanner_a.beacons[i_ab].add_possible_matches((i_ba, i_bb))
                            
                # we have the possible matchs, now identify which is the actual match
                for ia, beacon_a in enumerate(scanner_a.beacons):
                    ib = beacon_a.find_match_from_possible_matches()
                    if ib is not None:
                        beacon_b = scanner_b.beacons[ib]
                        
                        a_id = beacon_a.id
                        b_id = beacon_b.id
                        if a_id is None:
                            beacon_a.id = Beacon.generate_unique_id()
                            self.beacons[beacon_a.id] = {(ixa, ia),}
                        beacon_b.id = beacon_a.id
                        entry = self.beacons[beacon_a.id]
                        entry.add((ixb, ib))
                        self.beacons[beacon_a.id] = entry
                        
                for beacon in scanner_a.beacons:
                    beacon.clear_possible_matches()
        
        # we have generated unique beacon ids for each of the beacons we identified
        # as being seen by two or more scanners.  Now generate a unique id for each 
        # of the beacons that are observed by only one scanner.
        for scanner in self.scanners:   
            for i, beacon in enumerate(scanner.beacons):     
                if beacon.id is None:
                    beacon.id = Beacon.generate_unique_id()
                    self.beacons[beacon.id] = {(scanner.id, i)}
        
        # for beacon_id, pairs in self.beacons.items():
            # print(f"beacon_id {beacon_id:3d} {len(pairs)} pairs {pairs}")
        
        # include the unique beacon ids with the Beacon objects listed in each scanner
        for isx, scanner in enumerate(self.scanners):
            for ibx, beacon in enumerate(scanner.beacons):
                for bid, pairs in self.beacons.items():
                    for pair in pairs:
                        scanner_idx, beacon_idx = pair
                        if scanner_idx == isx and beacon_idx == ibx:
                            # this beacon is in this scanner
                            beacon.id = bid
        
        # for scanner in self.scanners:
            # print(f"Scanner {scanner.id:2d}")
            # for i, beacon in enumerate(scanner.beacons):
                # print(f"  {i:2d} Beacon id={beacon.id}")
        
        # go through the scanners and reorient their coordinate systems
        # to match Scanner 0.  A scanner that has not yet been reoriented
        # can be reoriented using any scanner which has already been reoriented 
        # (or scanner 0 which is the basis for orientation) and with which it has at
        # least two beacons in common        
        for ixa, scanner_a in enumerate(self.scanners):
            for ixb, scanner_b in enumerate(self.scanners[ixa+1:], ixa+1):
                if scanner_a.orientation is None and scanner_b.orientation is None:
                    continue
                if scanner_a.orientation is not None and scanner_b.orientation is not None:
                    continue
                common_beacons = []
                for beacon_a in scanner_a.beacons:
                    for beacon_b in scanner_b.beacons:
                        if beacon_a.id == beacon_b.id:
                            # found a match
                            common_beacons.append((beacon_a, beacon_b))
                            if len(common_beacons) == 2:
                                break
                    else:
                        # if we did not break out of the inner loop, continue the outer loop
                        continue
                    # if we did break out of the inner loop, then break out of the outer too
                    break
                else:
                    continue
                # have two common beacons for scanner_a and scanner_b
                # print(f"common_beacons for Scanner{scanner_a.id} and Scanner{scanner_b.id}")
                beacon_a_0, beacon_b_0 = common_beacons[0]
                beacon_a_1, beacon_b_1 = common_beacons[1]
                # print(f"   are {beacon_a_0} and {beacon_b_0}")
                # print(f"   and {beacon_a_1} and {beacon_b_1}")
                
                # we will reorient the scanner (of the two) that does not already have an orientation
                if scanner_a.orientation is not None:
                    scanner_a.transform_coordinates(scanner_b, beacon_a_0, beacon_a_1, beacon_b_0, beacon_b_1)
                else:
                    scanner_b.transform_coordinates(scanner_a, beacon_b_0, beacon_b_1, beacon_a_0, beacon_a_1)
        
        # now that all scanners have been oriented to match scanner 0, and have had their locations determined,
        # we can compute the 'absolute' location of each of the beacons.  Print the locations of all the beacons
        for beacon_id, pairs in self.beacons.items():
            # we need to use one of the members of this pairs set (it doesn't matter which one)
            # python has no elegant way to do that, but this kind of fake loop works
            for pair in pairs:
                break
            scanner_idx, beacon_idx = pair
            x, y, z = self.scanners[scanner_idx].absolute_location(beacon_idx)
            # print(f"For beacon_id {beacon_id:3d}, using Scanner {scanner_idx}, Beacon {beacon_idx}")
            # print(f"  absolute location is ({x},{y},{z})")
        
        # print the absolute locations of all the scanners
        # for scanner in self.scanners:
            # print(f"Scanner {scanner.id} location = {scanner.location}")
        
        # knowing the absolute locations of all the scanners, makes it easy to find the largest
        # 'Manhattan' distance (the sum of the x, y and z distances) between any pair of scanners
        self.max_manhattan = 0    
        for ixa, scanner_a in enumerate(self.scanners):
            for ixb, scanner_b in enumerate(self.scanners[ixa+1:], ixa+1):
                ax = scanner_a.location[0]
                ay = scanner_a.location[1]
                az = scanner_a.location[2]
                bx = scanner_b.location[0]
                by = scanner_b.location[1]
                bz = scanner_b.location[2]
                dx = abs(ax-bx)
                dy = abs(ay-by)
                dz = abs(az-bz)
                manhattan = dx + dy + dz
                if manhattan > self.max_manhattan:
                    self.max_manhattan = manhattan
                    sa = ixa
                    sb = ixb
        self.max_manhattan = (self.max_manhattan, sa, sb)            
                    

    def puzzle_part1(self):
        """run  part1 of puzzle"""
        
        print(f"{Beacon.unique_beacon_id} unique beacons found")

        
    
    def puzzle_part2(self):
        """run part2 of puzzle"""
        
        max_manhattan, sa, sb = self.max_manhattan
        print(f"Largest Manhattan distance between two scanners is {max_manhattan}")
        print(f" for Scanner {sa} and Scanner {sb}")
        
        
    def prepare_input_list(self, lines):
        """create a list of the input"""
        return lines

class Scanner():

    @classmethod
    def generator(cls, lines):
        """generate a sequence of Scanners from the input lines"""
        for line in lines:
            if line == '':
                # end of scanner
                yield Scanner(scanner_number, beacon_list)
            elif line[0:2] == '--':
                # start of new scanner
                # get '---', 'scanner', 'nn', '---'
                line = line.split()
                scanner_number = int(line[2])
                beacon_list = []
            else:
                # beacon line
                line = line.split(',')
                coords = tuple(int(v) for v in line)
                beacon_list.append(Beacon(coords))


    def __init__(self, scanner_num, beacons):
        """initialize Scanner object"""
        self.id = scanner_num
        self.orientation = ((+1, 0), (+1, 0), (+1, 0)) if scanner_num == 0 else None
        self.location = (0, 0, 0) if scanner_num == 0 else None
        self.beacons = beacons
        

    def beacon_pairs(self):
        """generate all pairs of beacons for this scanner"""
        
        for i_a, beacon_a in enumerate(self.beacons):
            for i_b, beacon_b in enumerate(self.beacons[i_a+1:], i_a+1):
                yield ((i_a, beacon_a), (i_b, beacon_b))

    def transform_coordinates(self, scanner_b, beacon_a_0, beacon_a_1, beacon_b_0, beacon_b_1):
        """find the orientation of a scanner and transform its coordinate system"""
        orientations = (
                    ((+1, 0), (+1, 1), (+1, 2)),
                    ((+1, 0), (+1, 2), (+1, 1)),
                    ((+1, 1), (+1, 0), (+1, 2)),
                    ((+1, 1), (+1, 2), (+1, 0)),
                    ((+1, 2), (+1, 0), (+1, 1)),
                    ((+1, 2), (+1, 1), (+1, 0)),
                    
                    ((+1, 0), (+1, 1), (-1, 2)),
                    ((+1, 0), (+1, 2), (-1, 1)),
                    ((+1, 1), (+1, 0), (-1, 2)),
                    ((+1, 1), (+1, 2), (-1, 0)),
                    ((+1, 2), (+1, 0), (-1, 1)),
                    ((+1, 2), (+1, 1), (-1, 0)),
                    
                    ((+1, 0), (-1, 1), (+1, 2)),
                    ((+1, 0), (-1, 2), (+1, 1)),
                    ((+1, 1), (-1, 0), (+1, 2)),
                    ((+1, 1), (-1, 2), (+1, 0)),
                    ((+1, 2), (-1, 0), (+1, 1)),
                    ((+1, 2), (-1, 1), (+1, 0)),
                    
                    ((+1, 0), (-1, 1), (-1, 2)),
                    ((+1, 0), (-1, 2), (-1, 1)),
                    ((+1, 1), (-1, 0), (-1, 2)),
                    ((+1, 1), (-1, 2), (-1, 0)),
                    ((+1, 2), (-1, 0), (-1, 1)),
                    ((+1, 2), (-1, 1), (-1, 0)),
                    
                    ((-1, 0), (+1, 1), (+1, 2)),
                    ((-1, 0), (+1, 2), (+1, 1)),
                    ((-1, 1), (+1, 0), (+1, 2)),
                    ((-1, 1), (+1, 2), (+1, 0)),
                    ((-1, 2), (+1, 0), (+1, 1)),
                    ((-1, 2), (+1, 1), (+1, 0)),
                    
                    ((-1, 0), (+1, 1), (-1, 2)),
                    ((-1, 0), (+1, 2), (-1, 1)),
                    ((-1, 1), (+1, 0), (-1, 2)),
                    ((-1, 1), (+1, 2), (-1, 0)),
                    ((-1, 2), (+1, 0), (-1, 1)),
                    ((-1, 2), (+1, 1), (-1, 0)),
                    
                    ((-1, 0), (-1, 1), (+1, 2)),
                    ((-1, 0), (-1, 2), (+1, 1)),
                    ((-1, 1), (-1, 0), (+1, 2)),
                    ((-1, 1), (-1, 2), (+1, 0)),
                    ((-1, 2), (-1, 0), (+1, 1)),
                    ((-1, 2), (-1, 1), (+1, 0)),
                    
                    ((-1, 0), (-1, 1), (-1, 2)),
                    ((-1, 0), (-1, 2), (-1, 1)),
                    ((-1, 1), (-1, 0), (-1, 2)),
                    ((-1, 1), (-1, 2), (-1, 0)),
                    ((-1, 2), (-1, 0), (-1, 1)),
                    ((-1, 2), (-1, 1), (-1, 0)) )
                    
                   
        
        delta_base_x = beacon_a_0.coords[0] - beacon_a_1.coords[0]
        delta_base_y = beacon_a_0.coords[1] - beacon_a_1.coords[1]
        delta_base_z = beacon_a_0.coords[2] - beacon_a_1.coords[2]
        
        coords_0 = beacon_b_0.coords
        coords_1 = beacon_b_1.coords
        
        for trans in orientations:
            trans_x, trans_y, trans_z = trans
            sx, tx = trans_x
            sy, ty = trans_y
            sz, tz = trans_z
            delta_x = (sx * coords_0[tx]) - (sx * coords_1[tx]) 
            delta_y = (sy * coords_0[ty]) - (sy * coords_1[ty])
            delta_z = (sz * coords_0[tz]) - (sz * coords_1[tz])
            if delta_base_x == delta_x and delta_base_y == delta_y and delta_base_z == delta_z:
                # print("Orientation Transform found:")
                # print(f"   matrix={trans}")
                # print(f"   base_0  {beacon_a_0.coords}  {beacon_a_1.coords}")
                # print(f"   coord   {coords_0}  {coords_1}")
                # print(f"            becomes")
                c_0 = (sx*coords_0[tx], sy*coords_0[ty], sz*coords_0[tz])
                # c_1 = (sx*coords_1[tx], sy*coords_1[ty], sz*coords_1[tz])
                # print(f"   trans   {c_0}  {c_1}")
                
                scanner_b.orientation = trans
                # update all of scanner_b's beacons to the new orientation
                # but leave the locations relative to scanner_b
                for beacon in scanner_b.beacons:
                    beacon.reorient(trans)
                    
                bx, by, bz = c_0
                ax, ay, az = beacon_a_0.coords
                x = self.location[0] + (ax - bx)
                y = self.location[1] + (ay - by)
                z = self.location[2] + (az - bz)
                scanner_b.location = (x, y, z)
                # print(f"Scanner {scanner_b.id} location set to ({x},{y},{z})")
                
                
    def absolute_location(self, beacon_idx):
        """compute the absolute location of a beacon (absolute means relative to Scanner 0)"""
        beacon = self.beacons[beacon_idx]
        x = self.location[0] + beacon.coords[0]
        y = self.location[1] + beacon.coords[1]
        z = self.location[2] + beacon.coords[2]
        return (x,y,z)         
            

    def __contains__(self, beacon_id):
        """returns True if the Scanner sees a beacon with this beacon_id"""
        for beacon in self.beacons:
            if beacon.id == beacon_id:
                return True
        return False
        
    def __str__(self):
        """format the Scanner object for printing"""
        ret_str = f"Scanner {self.id}"
        for beacon in self.beacons:
            ret_str += f"\n  Beacon {beacon}"
        return ret_str
    
    def __repr__(self):
        return self.__str__()    

class Beacon():
    """class to implement a beacon object"""
    unique_beacon_id = 0
    
    @classmethod
    def generate_unique_id(cls):
        """generate a unique beacon id """
        cls.unique_beacon_id += 1
        return cls.unique_beacon_id
        
    def __init__(self, beacon_coords):
        """initialize the beacon"""
        self.id = None
        self.coords = beacon_coords
        self.clear_possible_matches()
    
    def clear_possible_matches(self):
        """reset the possible matches"""
        self.possible_matches = []
        
    def add_possible_matches(self, possible_matches):
        """add a pair of beacons as a possible match with a pair from this beacon"""
        for p in possible_matches:
            self.possible_matches.append(p)

    def find_match_from_possible_matches(self):
        """find a match, if there is one, from among the possible matches
           if a possible match appears twice (meaning it matches in multiple scanners)
           then it is, in fact, a match
        """
        max_match = 0
        for v in self.possible_matches:
            if v > max_match:
                max_match = v
        if max_match == 0:
            return None
            
        match_counts = [0] * (max_match+1)
        for v in self.possible_matches:
            match_counts[v] += 1
        for i in range(max_match+1):
            if match_counts[i] > 1:
                return i
        return None

    def reorient(self, trans):
        """translate the coordinates of a beacon as seen by a scanner, to align the
           coordinate system with scanner 0
        """
        trans_x, trans_y, trans_z = trans
        sx, tx = trans_x
        sy, ty = trans_y
        sz, tz = trans_z
        self.coords = (sx*self.coords[tx], sy*self.coords[ty], sz*self.coords[tz])

        
    def __str__(self):
        return f"({self.coords[0]:5d},{self.coords[1]:5d},{self.coords[2]:5d})"  
        
    def __repr__(self):
        return self.__str__()
        
    @staticmethod
    def distance_squared(beacon_a, beacon_b):
        """compute the square of the distance between two beacons as seen by one scanner"""
        x = beacon_a.coords[0] - beacon_b.coords[0]
        y = beacon_a.coords[1] - beacon_b.coords[1]
        z = beacon_a.coords[2] - beacon_b.coords[2]
        return (x*x) + (y*y)+ (z*z)
       
    
# import code common for all Advent puzzles
import advent 
# pass module name, and package
advent.startup(__name__, __package__, obj=True)

