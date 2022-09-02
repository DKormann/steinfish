from fourinarow import FourInaRow
from players import Player, Console


def game(playerA:Player, playerB:Player, game_type = FourInaRow):
    next_player,last_player = playerA,playerB
    board = game_type()
    while board.winner == 0:
        board.make_move(next_player.choose_move(board))
        next_player,last_player = last_player,next_player 
    return board


def console_game():
    return game(Console(), Console())


if __name__ == "__main__":
    console_game()