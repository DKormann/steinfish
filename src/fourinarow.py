import numpy as np
from typing import List

from .base_classes import GameBoard


width = 7
height = 6
start_data = np.zeros((height,width))


#generate winning conditions ahead of time
def generate_winning_conditions():

    down_offsets = np.array([[1,2,3],[0,0,0]])
    right_offsets = np.array([[0,0,0],[1,2,3]])
    left_offsets = - right_offsets
    left_down_offsets = left_offsets+down_offsets
    right_down_offsets = right_offsets +down_offsets


    def add_check(conditions,offsets,row,column):
        arr = offsets+np.array([row,column]).repeat(3).reshape([2,-1])
        conditions.append(arr)

    conditions = []
    for row in range(height):
        row_conditions = []
        for column in range(width):
            tile_conditions = []
            if row <=height - 4:
                #checkdown
                add_check(tile_conditions,down_offsets,row,column)

                if column >=4-1:
                    #check left and down
                    add_check(tile_conditions, left_down_offsets,row,column)
                    add_check(tile_conditions,left_offsets,row,column)
                if column <= width - 4:
                    #check right and down
                    add_check(tile_conditions,right_down_offsets,row,column)
                    add_check(tile_conditions, right_offsets,row,column)
            else:
                if column >=4-1:
                    #check left and down
                    add_check(tile_conditions,left_offsets,row,column)
                if column <= width - 4:
                    #check right and down
                    add_check(tile_conditions, right_offsets,row,column)
            tile_conditions = np.concatenate(tile_conditions)

            row_conditions.append((
                tile_conditions[0::2],
                tile_conditions[1::2]
                ))

        conditions.append(row_conditions)
    return conditions

winning_conditions = generate_winning_conditions()



class FourInaRow(GameBoard):

    players = [1,-1]

    def __init__(self,data = None,turn:int = 0):
        if type(data) != np.ndarray:
            data  = start_data.copy()
        self.turn = turn
        self.data = data
        self.next_player = self.players[turn%2]
        self.last_player = self.players[(turn+1)%2]
        self.winner = 0
        self.possible_moves = np.where(self.data[0,:] == 0)[0]
        if self.possible_moves.shape == (0,):
            self.winner = 2



    def __repr__(self):

        """print out ui representation
        self.data is 6x7 matrix represented as 42 dim np array
        """

        tiles = {0:'  ',1:'❎',-1:'🅾️ '}

        res = ''

        for row in self.data:
            res += '||'
            for tile in row:
                res += tiles[tile]
            res += '||\n'
        res += '||'+'='*14+'||\n'
        res += '||0 1 2 3 4 5 6 ||\n'

        if self.winner !=0:
            res += f"\ngame over. {tiles[self.winner]} won.\n"
        else:
            res += f"\nnext move: {tiles[self.next_player]}"

        return res

    def make_move(self,move:int) -> int :
        """make a move on the given row for the next player in column"""

        assert self.data[0,move] == 0, f"error no more space on column {move}"


        data = self.data.copy()
        row =  np.where(self.data[:,move] == 0)[0][-1]

        data[row,move] = self.next_player
        result:FourInaRow= FourInaRow(data,self.turn +1)

        # print(row)

        #check whether the last move ended the game
        own_winning_conditions = winning_conditions[row][move]
        gameover = (result.data[own_winning_conditions]== self.next_player).all(1).any()
        if gameover:
            result.winner = self.next_player
        
        
        return result


example_board = FourInaRow( np.array([
    [0,0,0,0,0,0,0,],
    [0,0,0,0,0,0,0,],
    [0,0,0,0,0,0,0,],
    [0,0,0,-1,1,0,0,],
    [-1,0,0,1,-1,0,0,],
    [1,0,1,1,-1,0,0,],
]))
