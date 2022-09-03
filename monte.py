import numpy as np
from fourinarow import FourInaRow
from players import Player

class Monte(Player):

    """Monte carlo player"""

    def __init__(self):
        
        #employ dynamic programming so we remember searched states
        self.memory = {}
    
    def choose_move(self, game_board:FourInaRow):
        
        options = game_board.possible_moves
        

class SearchNode:
    pass
