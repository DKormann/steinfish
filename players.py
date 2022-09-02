from fourinarow import FourInaRow


class Player:
    """Player class can be derived by console or ai players."""
    def choose_move(self,game_board):
        """choose a valid move for a given game board"""
        pass


class Console(Player):

    def choose_move(self,game_board:FourInaRow):
        print(game_board)
        options = game_board.get_possible_moves()

        choice = int (input ("choose move 0-6: "))
        while choice not in options:
            print(options)
            print(f"illegal move. possible moves are: {', '.join(map(lambda x: int(x),list(options)))}")
            choice = int(input("choose move: "))

        return choice