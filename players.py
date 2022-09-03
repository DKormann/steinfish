from fourinarow import FourInaRow


class Player:
    """Player class can be derived by console or ai players."""
    def choose_move(self,game_board):
        """choose a valid move for a given game board"""
        pass


class Console(Player):

    def choose_move(self,game_board:FourInaRow):
        print(game_board)
        options = game_board.possible_moves


        choice = input ("choose move 0-6: ")
        try:
            choice = int(choice)
        except:
            if choice == 'f':
                choice = -1
        while choice not in list(options)+[-1]:

            print(f"illegal move. possible moves are: {options}\npress 'f' to give up")


            choice = input('choose move: ')
            try:
                choice = int(choice)
            except:

                if choice == 'f':
                    choice = -1
                    break
            
        return choice