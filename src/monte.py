from __future__ import annotations
from math import log, sqrt
import numpy as np
from .fourinarow import FourInaRow
from .base_classes import Player, GameBoard
from typing import List

class Monte(Player):

    """Monte carlo player"""

    def __init__(self):
        pass
    
    def choose_move(self, game_board:FourInaRow):
        
        root = SearchNode(game_board)

        for i in range (1000):
            root.expand()
        return root.get_best_move()



class SearchNode:

    def __init__(self,board:FourInaRow):
        self.board:FourInaRow = board
        self.ucb = float('inf')
        self.n = 0
        self.res = 0
        self.mu = 0
        self.options = board.possible_moves
        self.children:List[SearchNode] = []


    
    def expand(self)->int:
        # monte carlo tree search 

        res = 0
        if self.board.winner != 0:
            # because 4inarow always is won with the last move we can assume that if the game is won the current player has won it.
            self.res += 1
            self.n += 1
            return 1

        if self.n == 0:
            # expand leaf node

            self.options = np.random.choice(self.options,self.options.shape[0],replace=False)


        if self.n < self.options.shape[0]:
            # discover new options
            new_move = self.options[self.n]
            new_board = self.board.make_move(new_move)
            new_node = SearchNode(new_board)
            self.children.append(new_node)
            
            res = - new_node.expand()
            
        else :
            #find best leaf to expand

            best_ucb = -float('inf')
            for child in self.children:
                ucb = child.mu + sqrt(2*log(self.n)/child.n)
                if best_ucb < ucb:
                    best_ucb = ucb
                    best_child = child
            res = - best_child.expand()
            

        self.res += res
        self.n += 1
        self.mu = self.res / self.n

        return res

    def get_best_move(self):
        # get best move by node mu

        best_mu = self.children[0].mu
        best_move_index = 0

        for i in range(len(self.children)):
            child = self.children[i]
            if child.mu > best_mu:
                best_mu = child.mu
                best_move_index = i
        return self.options[best_move_index]

            
        
