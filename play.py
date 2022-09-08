from src.game import game, Console
from src.agents.monte import Monte

# print(game(Monte(emotional=True),Console()))


def clash(player_a,player_b,k = 10):
    a_wins = 0
    b_wins = 0
    draws = 0
    def match(a,b):
        return (
            1 if res == 1 else 0,
            1 if res == -1 else 0,
            1 if res == 2 else 0,
        )

    
    for _ in range(0,k,2):

        res = game(player_a,player_b).winner
        a_wins += 1 if res == 1 else 0
        b_wins += 1 if res == -1 else 0
        draws += 1 if res == 2 else 0
        print(f"{type(player_a).__name__}: {a_wins},{type(player_b).__name__}: {b_wins}, draws: {draws}")


        res = game(player_b,player_a).winner
        b_wins += 1 if res == 1 else 0
        a_wins += 1 if res == -1 else 0
        draws += 1 if res == 2 else 0
        print(f"{type(player_a).__name__}: {a_wins},{type(player_b).__name__}: {b_wins}, draws: {draws}")


        
    

        
