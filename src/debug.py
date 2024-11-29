from ai import Strategist
import othello
import sys

game_state_at_crash = [
    ["B", "B", "B", "B", "B", "B", "B", "B", "B"],
    ["B", "B", "W", "W", "W", "W", "W", "W", "B"],
    ["B", "B", "W", "B", "B", "B", "W", "W", "B"],
    ["B", "B", "W", "B", "W", "W", "B", "W", "B"],
    ["B", "W", "B", "W", "W", "B", "B", "B", "B"],
    ["B", "B", "W", "B", "B", "B", "B", "B", "B"],
    ["B", "W", "W", "W", "W", "W", "W", ".", "B"],
]

if __name__ == "__main__":
    game = othello.OthelloGame(7, 9, "W")
    game.current_board = game_state_at_crash

    strategist = Strategist.Strategist()

    result, move = strategist.alpha_beta(0, game, -sys.maxsize, sys.maxsize, "W")

    print(result)
    print("-----------------------------------------")
    print(move)
