# description required by advent.py
description = (("Play a dice rolling game with a 'deterministic' die ",        # part 1
                "Get the product of the losing player's score and the number of times the die was rolled"),
               ("Play the game with a 'dirac' die, which splits the universe into three on every roll",        # part 2       
                "For the player with the most wins, find the number of universes in which that player won") 
              )
from functools import lru_cache
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
        self.initial_positions = self.prepare_input_list(lines)
        die = DeterministicDie(5)
        
            
    def puzzle_part1(self):
        """run  part1 of puzzle"""
        
        die = DeterministicDie(sides=100, default_rolls=3)
        players = [Player(pos, die) for pos in self.initial_positions]
            
        winner = None
        while winner is None:
            for player in players:
                if player.move() >= 1000:
                    winner = player
                    break
        
        for player in players:
            print(f"Player {player}")  
            if player.score < 1000:
                loser_score = player.score
        
        print()        
        print(f"roll count is  {die.roll_count}")
        print(f"loser score is {loser_score}")
        print()
        print(f"product is {die.roll_count * loser_score}")
            
    def puzzle_part2(self):
        """run part2 of puzzle"""
        
        player_1_pos, player_2_pos = self.initial_positions
        player_1_wins, player_2_wins = self.find_wins(player_1_pos-1, 0, player_2_pos-1, 0)
        
        print(f"Player 1 wins in {player_1_wins:20d} universes")
        print(f"Player 2 wins in {player_2_wins:20d} universes")
        print()
        print(self.find_wins.cache_info())


    # caching the results of this function improves the performance from approximately
    # three years down to just a few seconds.  This is because this recursive function
    # computes the same paths (from position and score to a win) literally billions of
    # times.  There really aren't that many unique paths.  Once they are calculated
    # we can just look up the results for whole trees of paths
    # to make the cache work, this function cannot depend on 'state' external to itself
    @lru_cache(maxsize=None)
    def find_wins(self, player_1_pos, player_1_score, player_2_pos, player_2_score):
        """find all the ways that player 1 and player 2 can win with these
           starting positions.  recursively solves for all possible positions
        """
        # if this position wins for player 1, then there is just one 
        # way to win from here, and no way for player 2 (since player 1 goes first)
        if player_1_score >= 21:
            return (1, 0)
        # player 2 wins from here
        if player_2_score >= 21:
            return (0, 1)
            
        count_player_1_wins = 0
        count_player_2_wins = 0
        
        # roll the die three times, and each roll has three possible outcomes
        # because this is a 'multiverse' universe, we have to account for all three
        # possible outcomes of each roll
        for roll1 in (1,2,3):
            for roll2 in (1,2,3):
                for roll3 in (1,2,3):
                    # move player 1 to the new position
                    new_player_1_pos = (player_1_pos + roll1 + roll2 + roll3) % 10
                    # compute player 1's new score
                    new_player_1_score = player_1_score + (new_player_1_pos + 1)
                    # now swap the player 1 and player 2 roles and so move player 2
                    player_2_count, player_1_count = self.find_wins(player_2_pos, player_2_score,
                                                                    new_player_1_pos, new_player_1_score)
                    # find_wins has found all wins for player 1 and for player 2 from the 
                    # starting positions and scores given by our caller
                    count_player_1_wins += player_1_count
                    count_player_2_wins += player_2_count
                    
        # now return the player 1 and player 2 counts to our caller
        return (count_player_1_wins, count_player_2_wins)
        
    def prepare_input_list(self, lines):
        """create a list of the input"""
        
        positions = [int(line.split()[4]) for line in lines]
        return positions


    


class Die:
    class NakedDie(Exception):
        """attempt to use Die with no 'roll' method"""
            
        def __str__(self):
            string = 'NakedDie: '
            nl = ''
            v = ''
            for arg in self.args:
                v += f"{nl}{string:10s} " + arg
                string = ''
                nl = '\n'
            return v
            
    def __init__(self, sides, default_rolls):
        self.sides = sides
        self.default_rolls = default_rolls
        self.roll_count = 0
        
    def roll(self, n=1):
        if n == 1:
            return _roll()
        rolls = [r for r in self.roll_n(n)]
        return rolls
        
    def _roll(self):
        raise Die.NakedDie('Cannot roll a naked die', 'and this too')
        
    def roll_n(self, n):
        for _ in range(n):
            yield self._roll()
    
    def reset(self, sides=None):
        self.roll_count = 0
        if sides is not None:
            self.sides = sides    
    
class DeterministicDie(Die):
    def __init__(self, sides, default_rolls=1):
        super().__init__(sides, default_rolls)
        self.prev = 0
    
    def _roll(self):
        self.roll_count += 1
        self.prev = (self.prev % self.sides) + 1
        return self.prev
        
        
    def reset(self, sides=None):
        super().reset(sides=sides)
        self.next = 0

class Player:
    
    player_id = 0
    
    def __init__(self, init_position, die):
        Player.player_id += 1
        self.id = Player.player_id
        self.reset(init_position)
        self.die = die
        
    def reset(self, init_position=None):
        self.score = 0
        if init_position is None:
            init_position = self.init_position
        self.init_position = init_position
        self.position = init_position
        
    def move(self, rolls=None):
        if rolls is None:
            rolls = self.die.default_rolls
        steps = sum(self.die.roll(rolls))
        self.position = ((self.position + steps - 1) % 10) + 1
        self.score += self.position
        return self.score
    
    def __str__(self):
        return f" {self.id}  position {self.position:2d}  score {self.score:4d}"

# import code common for all Advent puzzles
import advent 
# pass module name, and package
advent.startup(__name__, __package__, obj=True)

