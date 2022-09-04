from .fourinarow import FourInaRow
from .base_classes import Player,GameBoard


def game(playerA:Player, playerB:Player, game_type:GameBoard = FourInaRow):

    next_player,last_player = playerA,playerB

    players = {
        1:next_player,
        -1:last_player
    }
    board = game_type()
    while board.winner == 0:
        next_player = players[board.next_player]

        try:
            move = next_player.choose_move(board)
        except KeyboardInterrupt:
            print()
            break
        if move == -1:
            print("game forfitted")
            board.winner = board.last_player
            break
        board = board.make_move(move)

    return board


def console_game():
    return game(Console(), Console())


if __name__ == "__main__":
    console_game()



class Console(Player):

    def choose_move(self,game_board:GameBoard):
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