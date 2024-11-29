""" Example of a random AI. The class name has to be the same as the module name.
"""

from __future__ import (
    annotations,
)  # postpones the evaluation of the type hints, hence they do not need to be imported
import numpy as np
import othello
import sys

MAX_DEPTH = 5


class MaximumStoneStrategy:
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
        print(f"Maximum Stone : {possible_moves}")
        if len(possible_moves) > 1:
            _, move = self.go_down(
                0,
                board.copy_game(),
                board.get_turn(),
                -sys.maxsize,
                sys.maxsize,
            )
            return move
        else:
            return board.get_possible_move()[0]

    def evaluate(self, board: othello.OthelloGame, turn: str):
        value = {othello.BLACK: 0, othello.WHITE: 0, othello.NONE: 0}

        test = np.array(board.get_board()).flatten()
        for x in test:
            value[x] += 1

        if board.get_turn() == othello.BLACK:
            return value["B"] - value["W"]
        else:
            return value["W"] - value["B"]

    def go_down(
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
            return (self.evaluate(game, turn), move)

        new_depth = depth + 1
        return_move = None

        if depth % 2 == 1:
            value = sys.maxsize
            for move in game.get_possible_move():
                result, _ = self.go_down(
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
                result, _ = self.go_down(
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
        return "Maximum Stone"
