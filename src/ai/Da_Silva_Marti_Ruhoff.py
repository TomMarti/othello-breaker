""" Example of a random AI. The class name has to be the same as the module name.
"""

from __future__ import (
    annotations,
)  # postpones the evaluation of the type hints, hence they do not need to be imported
import numpy as np
import othello

MAX_DEPTH = 5


class Da_Silva_Marti_Ruhoff:
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
        test0, test1 = self.go_down(0, board.copy_game(), board.get_turn())
        print(test0, test1)
        return test1

    def evaluate(self, board: othello.OthelloGame, turn: str):
        value = {othello.BLACK: 0, othello.WHITE: 0, othello.NONE: 0}

        test = np.array(board).flatten()
        for x in test:
            value[x] += 1

        if turn == othello.BLACK:
            return value["B"] - value["W"]
        else:
            return value["W"] - value["B"]

    def go_down(
        self,
        depth: int,
        game: othello.OthelloGame,
        turn: str,
        move: tuple[int, int] = None,
    ) -> (int, tuple[int, int]):  # type: ignore
        if depth > MAX_DEPTH and move is not None:
            game.move(move[0], move[1])
            return (self.evaluate(game.get_board(), turn), move)

        value = []
        new_depth = depth + 1
        for move in game.get_possible_move():
            value.append(
                self.go_down(new_depth, game.copy_game(), self.update_turn(turn), move)
            )
        value.sort(key=lambda x: x[0])
        if depth % 2 == 0:
            return value[-1]
        else:
            return value[0]

    def update_turn(slef, turn):
        if turn == othello.BLACK:
            return othello.WHITE
        else:
            return othello.BLACK

    def __str__(self):
        return "Da_Silva_Marti_Ruhoff"
