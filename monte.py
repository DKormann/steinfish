import numpy as np
from fourinarow import FourInaRow
from players import Player

class Monte(Player):

    """Monte carlo player"""

    def __init__(self):
        pass
    
    def choose_move(self, game_board:FourInaRow):
        
        root = game_board

        for i in range (1000):
            root.expand()
        return root.best_option

        
        

class SearchNode:

    def __init__(self,board:FourInaRow):
        self.board = board
        self.ucb = 0
        self.options = self.board.possible_moves
        self.best_option = self.options[0]
        
    def expand(self):
        #TODO: implement monte carlo 
        pass


