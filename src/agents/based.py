from __future__ import annotations
from src.base_classes import GameBoard, Player

from src.fourinarow import FourInaRow
from .monte import Monte
from typing import Dict
from ..ucb import SearchNode

class Based(Monte):
    """monte carlo player with """


    database:Dict[int,Evaluation] = {}


    def loose(self):
        print("I LOOSE")
        self.learn(-1)

    def choose_move(self, game_board: FourInaRow):
        res = super().choose_move(game_board)
        print (self.root.mu)

        if self.root.best_child.board.winner not in [0,2]:
            # print('I WIN')
            self.learn(1)
        return (res)
    
    def learn(self,res):
        evaluation_node = self.root.best_child
        while evaluation_node != None:
            evaluation_hash = hash_board(evaluation_node.board)
            # print(evaluation_hash)
            if evaluation_hash in self.database:
                evaluation = self.database[evaluation_hash]
                evaluation.n += 1
                evaluation.r += res
            else:
                evaluation = Evaluation(1,res)
                self.database[evaluation_hash] = evaluation
            res = -res
            evaluation_node = evaluation_node.parent
        print(evaluation_node)

def hash_board(board:FourInaRow):

    hash1 = hash(str(board.data))
    flipped = board.data[:,::-1]
    hash2 = hash(str(flipped))
    return min(hash1,hash2)


class BasedSearch(SearchNode):

    def __init__(self, board: FourInaRow, parent:BasedSearch, agent:Based):
        super().__init__(board, parent)
        self.agent = agent


    def approximate(self, node: SearchNode):
        own_hash = hash_board(self.board)
        if own_hash in self.database:
            database_evaluation =  self.database[own_hash]
            return database_evaluation.r/database_evaluation.n
        return super().approximate()
        


class Evaluation:
    def __init__(self,n,r):
        self.n = n
        self.r = r