from __future__ import annotations
from ..fourinarow import FourInaRow
from ..base_classes import Player, GameBoard
from ..ucb import SearchNode

class Monte(Player):

    """Monte carlo player"""

    Search:type = SearchNode

    def __init__(self,emotional = True, search_depth = 2000):
        self.search_depth = search_depth
        self.emotional = emotional
        self.last_move = 0
        self.root = None


    def choose_move(self, game_board:FourInaRow):


        found = False

        if self.root :
            for child in self.root.best_child.children:
                if (child.board.data == game_board.data).all():

                    self.root = child
                    found = True
        
        if not found:
            self.root = self.Search(game_board,None,self)

        for i in range (self.search_depth):
            self.root.expand()



        if self.emotional:
            # print(f"emotion: {-round(100*root.mu,2)}")

            winning_percentage = round(-50*self.root.mu,2)+50
            face = ''
            if winning_percentage > 95:
                face = '😝'
            elif winning_percentage > 90:
                face = '😁'
            elif winning_percentage > 70:
                face = '😎'
            elif winning_percentage > 50:
                face = '🙂'
            elif winning_percentage > 30:
                face = '🤨'
            elif winning_percentage > 10:
                face = '😖'
            elif winning_percentage > 5 :
                face = '😓'
            else:
                face = '😵'

            print (f'\n {face}\n')

        best_move = self.root.get_best_move()
        # print(self.root.best_child)

        return best_move

