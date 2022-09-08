from __future__ import annotations
import numpy as np
from math import sqrt, log
from src.base_classes import GameBoard, Player
from src.fourinarow import FourInaRow
from .monte import Monte
from typing import Dict,Tuple
from ..ucb import SearchNode

from src.fourinarow import hash_board

import pickle

class Based(Monte):
    """monte carlo player with """

    # Search: type = BasedSearch
    # database:Dict[int,Tuple[int,int]] = {}

    def __init__(self, emotional=True, search_depth=2000):
        super().__init__(emotional, search_depth)
        self.Search  = BasedSearch
        self.load()

    def load(self,location = 'database/data.json'):
        file = open(location,'rb')
        self.database = pickle.load(file)
        file.close()

    def save(self,location = 'database/data.json'):
        file = open(location,'wb')
        pickle.dump(self.database,file)
        file.close()


    def end(self,value):
        if value == -1:
            self.learn(-1)
        elif value == 1:
            self.learn(1)

    def choose_move(self, game_board: FourInaRow):
        res = super().choose_move(game_board)
        return res
    
    def learn(self,res):
        evaluation_node = self.root.best_child
        while evaluation_node != None:
            evaluation_hash = hash_board(evaluation_node.board.data)
            if evaluation_hash == -6835557790018719421:
                print('learn start')
            if evaluation_hash in self.database:

                evaluation = self.database[evaluation_hash]
                self.database[evaluation_hash] = [
                    evaluation[0] + 1,
                    evaluation[1] + res
                ]
            else:
                evaluation = [1,res]
                self.database[evaluation_hash] = evaluation
            res = -res
            evaluation_node = evaluation_node.parent
        print(evaluation_node)


class BasedSearch(SearchNode):

    def __init__(self, board: FourInaRow, parent:BasedSearch, agent:Based):
        super().__init__(board, parent)
        self.agent = agent


    def approximate(self, node: SearchNode):
        own_hash = hash_board(self.board.data)
        if own_hash in self.agent.database:
            database_evaluation =  self.agent.database[own_hash]

            mean = - database_evaluation[1]/database_evaluation[0]
            # print(f"BD HIT {mean} * {database_evaluation[0]}")
            node.n += 1
            return mean
        return super().approximate(node)
    
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
            new_node = BasedSearch(new_board,parent= self,agent = self.agent)
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
