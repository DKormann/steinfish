from turtle import down
import numpy as np
from typing import List

from .base_classes import GameBoard


width = 7
height = 6
start_data = np.zeros((height,width))


#generate winning conditions ahead of time
def generate_winning_conditions():
    
    a = np.array([0,1,2,3])
    z = np.array([0,0,0,0])

    directions = np.array([
        [a,z],
        [a,a],
        [z,a],
        [a,-a]
    ])

    conditions = [None]*height


    for row in range(height):
        conditions [row] = [None] * width
        for column in range(width):
            
            tile_conditions:List[np.ndarray] = []

            for dir in directions:

                x = row
                y = column

                dirx = dir[0]
                diry = dir[1]

                for i in range(4):
                    # x -= dirx [i]
                    # y -= diry [i]
                

                    dirx = dir[0]
                    diry = dir[1]
                    dir = np.array([
                        
                        dirx + x - dirx[i],
                        diry + y - diry[i]])
                    
                    if (dir[0]>=0).all() and (dir[0] < height).all() and (dir[1] >=0).all() and (dir[1] < width).all():

                        tile_conditions.append(dir)

            tile_conditions = np.concatenate(tile_conditions)

                
            # print(row,column,len(conditions))
            conditions[row][column] = (tile_conditions[0::2],tile_conditions[1::2])

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
        res += '||'+'='*width*2+'||\n'
        res += f'|| { " ".join(map(lambda x: str(x),range(width)))}||\n'

        if self.winner == 2:
            res += f"\ndraw."
        elif self.winner !=0:
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
