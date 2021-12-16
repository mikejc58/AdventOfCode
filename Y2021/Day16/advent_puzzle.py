# description required by advent.py
description = (("Parse the binary transmission into packets",        # part 1
                "compute the sum of the packet versions"),
               ("Parse the binary transmission into packets",        # part 2    
                "compute the value of the base packet")   
              )


# to run:
#   put advent_puzzle.py and advent.py into a folder
#   navigate to that folder
#   execute  python3 advent_puzzle.py

#   advent.py contains functions that are (will be common) to all of the puzzles
#   and advent.py and advent_puzzle.py have some complications because I have set
#   them up to be able to be executed in a batch with more puzzles.  You can ignore
#   that.  

class BitsExhausted(Exception):
    pass

class AdventPuzzle():
    def __init__(self, lines):
        """initialize the AdventPuzzle object"""
        self.lines = self.prepare_input_list(lines)
        bitstrings = [Bits(convert_to_binary(packet_string)) for  packet_string in self.lines]
        
        self.base_packets = [Packet(bits) for bits in bitstrings]
        
        print()
        for packet in self.base_packets:
            print(packet, '\n')
        
    def puzzle_part1(self):
        """run  part1 of puzzle"""
        for packet in self.base_packets:
            print(f"version sum={packet.version_sum}")
       

    def puzzle_part2(self):
        """run part2 of puzzle"""
        for packet in self.base_packets:
            print(f"packet value={packet.value}")
        
        
    def prepare_input_list(self, lines):
        """create a list of the input"""
        return lines

hex_to_bit = {'0': '0000', '1': '0001', '2': '0010', '3': '0011', '4': '0100', '5': '0101', '6': '0110', '7': '0111',
              '8': '1000', '9': '1001', 'A': '1010', 'B': '1011', 'C': '1100', 'D': '1101', 'E': '1110', 'F': '1111'}

def convert_to_binary(packet_string):
    """convert a hexadecimal string into a bit string"""
    return ''.join([hex_to_bit[c] for c in packet_string])

class Bits():
    """object to contain a bit string and feed bits to callers"""
    def __init__(self, bit_string):
        self.bits = bit_string
        
    
    def get(self, bits):
        """get and remove bits from the Bits object"""
        if len(self.bits) >= bits:
            ret_value = self.bits[:bits]
            self.bits = self.bits[bits:]
        else:
            raise BitsExhausted(f"{bits} bits requested, {len(self.bits)} available")
        return ret_value


def packet_gen(bits, limit=None):
    """generate packets until limit is reached or we run out of bits"""
    generated = 0
    while True:
        
        try:
            packet = Packet(bits)
        except BitsExhausted:
            break
            
        yield packet
        
        if limit is not None:
            generated += 1
            if generated == limit:
                break
            

class Packet():
    """object to represent a packet and its sub-packets"""
    def __init__(self, bits):
        """build the packet from the bits object"""
        self.version = int(bits.get(3), 2)
        self.ptype = int(bits.get(3), 2)
        self.subpackets = []
        self.value = None
        
        if self.ptype == 4:
            # numeric literal
            self.value = 0
            while True:
                more = bits.get(1)
                digit = bits.get(4)
                self.value = (self.value * 16) + int(digit, 2)
                if more == '0':
                    break
            
        else:
            # operator does mathematical operations on the subpackets
            # create all the subpackets
            length_type = bits.get(1)
            if length_type == '0':
                # length of subpackets specified
                sub_len = int(bits.get(15), 2)
                # extract sub_len bits from the bits object
                sub_bits = Bits(bits.get(sub_len))
                # generate sub_packets from the sub_len bits until there are not enough
                # left to create any more sub_packets
                self.subpackets = [packet for packet in packet_gen(sub_bits)]
                
            else:
                # number of subpackets specified
                sub_num = int(bits.get(11), 2)
                # generate the number of sub_packets specified
                self.subpackets = [packet for packet in packet_gen(bits, limit=sub_num)]
            
            # perform the operation on the subpackets        
            if self.ptype == 0:
                # compute sum of the subpackets
                self.value = 0
                for subpacket in self.subpackets:
                    self.value += subpacket.value
            elif self.ptype == 1:
                # compute product of the subpackets
                self.value = 1
                for subpacket in self.subpackets:
                    self.value *= subpacket.value
            elif self.ptype == 2:
                # compute the minimum of the subpackets
                self.value = None
                for subpacket in self.subpackets:
                    if self.value is None or subpacket.value < self.value:
                        self.value = subpacket.value
            elif self.ptype == 3:
                # compute the maximum of the subpackets
                self.value = None
                for subpacket in self.subpackets:
                    if self.value is None or subpacket.value > self.value:
                        self.value = subpacket.value
            elif self.ptype == 5:
                # return 1 if subpacket[0] > subpacket[1] else 0
                self.value = 1 if self.subpackets[0].value > self.subpackets[1].value else 0
            elif self.ptype == 6:
                # return 1 if subpacket[0] < subpacket[1] else 0
                self.value = 1 if self.subpackets[0].value < self.subpackets[1].value else 0
            elif self.ptype == 7:
                # return 1 if subpacket[0] == subpacket[1] else 0
                self.value = 1 if self.subpackets[0].value == self.subpackets[1].value else 0
        
        self.version_sum = self.version
        for subpacket in self.subpackets:
            self.version_sum += subpacket.version_sum
                        
    
    def __str__(self):
        my_string = f"Packet: vers={self.version}, type={self.ptype}, value={self.value}, sub_packets={len(self.subpackets)}"
        if (len(self.subpackets) > 0):
            my_string += f"\n  sub Packets:"
        for subpacket in self.subpackets:
            sub_string = subpacket.__str__()
            sub_string_list = sub_string.split('\n')
            for sub in sub_string_list:
                my_string += f"\n    {sub}"
        return my_string
        
# import code common for all Advent puzzles
import advent 
# pass module name, and package
advent.startup(__name__, __package__, obj=True)

