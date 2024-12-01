"""Example of a random AI. The class name has to be the same as the module name."""

from __future__ import (
    annotations,
)  # postpones the evaluation of the type hints, hence they do not need to be imported
import numpy as np
import othello
import sys

MAX_DEPTH = 5
MOVES = {
    0: (0, 1),
    1: (1, 1),
    2: (1, 0),
    3: (1, -1),
    4: (0, -1),
    5: (-1, -1),
    6: (-1, 0),
    7: (-1, 1),
}


class MaximumStoneStrategyOptimized:
    """The name of this class must be the same as its file."""

    def __init__(self):
        pass

    def next_move(self, board: othello.OthelloGame) -> tuple[int, int]:
        """Returns the next move to play.

        Args:
            board (othello.OthelloGame): _description_

        Returns:
            tuple[int, int]: the next move (for instance: (2, 3) for (row, column), starting from 0)
        """
        possible_moves = set(board.get_possible_move())
        if len(possible_moves) > 1:
            _, move = self.alpha_beta(
                0,
                board.copy_game(),
                board.get_turn(),
                -sys.maxsize,
                sys.maxsize,
            )
            return move
        else:
            board.get_possible_move()[0]

    def evaluate(self, board: othello.OthelloGame, turn: str):
        value = {othello.BLACK: 0, othello.WHITE: 0, othello.NONE: 0}

        test = np.array(board).flatten()
        for x in test:
            value[x] += 1

        if turn == othello.BLACK:
            return value["B"] - value["W"]
        else:
            return value["W"] - value["B"]

    def next_direction_to_check(self, counter):
        """
        Utility method for move_value() function, private use
        """

        if counter not in MOVES:
            raise IndexError("Illegal Counter")

        direction = MOVES[counter]
        return direction[0], direction[1]

    def move_value(self, board: othello.OthelloGame, move: tuple[int, int]) -> int:
        """
        Evaluate the move value by exploring only necessary case
        """

        work_board = board.get_board()
        current_player = board.turn
        opponent = "W"
        if current_player == "W":
            opponent = "B"

        value = 0  # The placed piece is not counted, change to one for that

        for counter in range(0, 8):
            x, y = self.next_direction_to_check(counter)
            base_position_x = move[0]
            base_position_y = move[1]
            value_to_maybe_add = 0

            next_x = base_position_x
            next_y = base_position_y

            while True:
                next_x = next_x + x
                next_y = next_y + y

                try:
                    color_next_case = work_board[next_x][next_y]
                    if color_next_case == current_player:
                        value += value_to_maybe_add
                        break
                    elif color_next_case == opponent:
                        value_to_maybe_add += 1
                    elif color_next_case == ".":
                        break
                except IndexError:
                    # Out of bound, no gain
                    break

        return value

    def alpha_beta(
        self,
        depth: int,
        game: othello.OthelloGame,
        turn: str,
        alpha: int,
        beta: int,
        move: tuple[int, int] = None,
    ) -> (int, tuple[int, int]):  # type: ignore
        if move is not None:
            game.move(move[0], move[1])

        if depth > MAX_DEPTH:
            return (self.move_value(game, move), move)

        new_depth = depth + 1
        return_move = None

        if depth % 2 == 1:
            value = sys.maxsize
            for move in game.get_possible_move():
                result, _ = self.alpha_beta(
                    new_depth,
                    game.copy_game(),
                    self.update_turn(turn),
                    alpha,
                    beta,
                    move,
                )
                if value > result:
                    return_move = move
                    value = result

                if alpha >= value:
                    return (value, return_move)
                beta = min(beta, value)
        else:
            value = -sys.maxsize
            for move in game.get_possible_move():
                result, _ = self.alpha_beta(
                    new_depth,
                    game.copy_game(),
                    self.update_turn(turn),
                    alpha,
                    beta,
                    move,
                )
                if value < result:
                    return_move = move
                    value = result
                if beta <= value:
                    return (value, return_move)
                alpha = max(alpha, value)
        return (value, return_move)

    def update_turn(slef, turn):
        if turn == othello.BLACK:
            return othello.WHITE
        else:
            return othello.BLACK

    def __str__(self):
        return "Maximum Stone strategy"
