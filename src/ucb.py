from __future__ import annotations
from .fourinarow import FourInaRow
import numpy as np
from math import log,sqrt
from typing import List

class SearchNode:


    def __init__(self,board:FourInaRow,parent,agent = None):
        self.parent = parent
        # assert self.parent != None
        self.board:FourInaRow = board
        self.ucb = float('inf')
        self.n = 0
        self.res = 0
        self.mu = 0
        self.options = board.possible_moves
        self.children:List[SearchNode] = []

    def approximate(self,node:SearchNode):
        res = - node.expand()
        return res

    
    def expand(self)->int:
        # monte carlo tree search 

        res = 0
        if self.board.winner != 0:
            if self.board.winner == 2:
                self.n += 1
                self.res = 0
                return 0
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
            new_node = SearchNode(new_board,parent= self)
            self.children.append(new_node)
            res = self.approximate(new_node)

            
        else :

            #find best leaf to expand

            best_ucb = -float('inf')
            for child in self.children:
                ucb = child.mu + sqrt(2*log(self.n)/child.n)
                if best_ucb < ucb:
                    best_ucb = ucb
                    best_child = child
            res = - best_child.expand()

            # if self.n == self.options.shape[0]:
                # print(best_child.board)

        self.res += res
        self.n += 1
        self.mu = self.res / self.n

        return res

    def get_best_move(self):
        # get best move by node mu

        best_mu = self.children[0].mu
        self.best_child = self.children[0]
        best_move_index = 0

        for i in range(len(self.children)):
            child = self.children[i]
            if child.mu > best_mu:
                best_mu = child.mu
                self.best_child = child
                best_move_index = i
        return self.options[best_move_index]

    def __hash__(self):
        return hash(str(self.board.data))

    def __repr__(self):
        board_repr = str(self.board).split('\n')
        board_repr[0] += f' n: {self.n}'
        board_repr[1] += f' mu: {self.mu}'

        return '\n'.join(board_repr)
        
