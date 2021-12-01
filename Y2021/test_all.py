import sys
import TimingManager as tm

# Test driver for Advent of Code  2021

mod_list = []

# each imported advent module will add itself to mod_list
import Day1.advent_puzzle


def test_all(input_file):
    
    # test all the modules imported above
    for mod, pack in mod_list:
        mod_name = mod.__name__
        # print(f'\nTesting {mod_name}  -  {mod.description}')
        print(f'\nTesting {mod_name}')
        # use TimingManager to get elapsed time for each part
        with tm.TimingManager(f'{mod_name} Part1', elapsedOnly=True):
            mod.puzzle(pack+'/'+input_file, part=1)
            
        with tm.TimingManager(f'{mod_name} Part2', elapsedOnly=True):
            mod.puzzle(pack+'/'+input_file, part=2)
    
if __name__ == '__main__':
    test_all('input.txt')
