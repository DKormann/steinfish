from fourinarow import FourInaRow
from players import Player, Console


def game(playerA:Player, playerB:Player, game_type = FourInaRow):

    players = {
        1:playerA,
        -1:playerB
    }
    next_player,last_player = playerA,playerB
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