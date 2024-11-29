"""Example of a random AI. The class name has to be the same as the module name."""

from __future__ import (
    annotations,
)  # postpones the evaluation of the type hints, hence they do not need to be imported
import othello
import sys
import numpy as np

MAX_DEPTH = 5
AVOIDED_CASE = [(1, 1), (7, 1), (1, 5), (7, 5)]
CORNER = [(0, 0), (8, 0), (0, 6), (8, 6)]
GAME_X = 8
GAME_Y = 6

CORNER_DIRECTION = {
    (0, 0): [(1, 0), (0, 1)],
    (8, 0): [(-1, 0), (0, 1)],
    (0, 6): [(1, 0), (0, -1)],
    (8, 6): [(-1, 0), (0, -1)],
}


class NoneCell(Exception):
    """Raised whenever a cell is None"""

    pass


class Strategist:
    """The name of this class must be the same as its file."""

    def __init__(self):
        pass

    def is_border(self, x, y, board):
        for y_delta in range(-1, 2):
            for x_delta in range(-1, 2):
                new_y = y + y_delta
                new_x = x + x_delta
                if 0 <= new_y < len(board) and 0 <= new_x < len(board[y]):
                    if board[new_y][new_x] == othello.NONE:
                        return 1
        return 0

    def get_border_value(self, game: othello.OthelloGame, player: str):
        value = 0
        board = game.get_board()
        for y in range(len(board)):
            for x in range(len(board[y])):
                if board[y][x] == player:
                    value += self.is_border(x, y, board)

        return value

    def get_other(self, player_turn: str) -> str:
        if player_turn == othello.BLACK:
            return othello.WHITE
        else:
            return othello.BLACK

    def get_stable_piece(self, game: othello.OthelloGame, player: str):
        value = 0
        board = game.get_board()
        for cell in CORNER:
            if cell == player:
                value += 1
                for dir in CORNER_DIRECTION:
                    x = cell[0]
                    y = cell[1]
                    while board[x][y] == player:
                        value += 1
                        x += dir[0]
                        x += dir[1]

        return value

    def next_move(self, board: othello.OthelloGame) -> tuple[int, int]:
        """Returns the next move to play.

        Args:
            board (othello.OthelloGame): _description_

        Returns:
            tuple[int, int]: the next move (for instance: (2, 3) for (row, column), starting from 0)
        """
        _, move = self.alpha_beta(
            0,
            board.copy_game(),
            -sys.maxsize,
            sys.maxsize,
            board.get_turn(),
        )
        return move

    def evaluate(self, game: othello.OthelloGame, move, player, turn_number=0) -> float:
        if move in CORNER:
            if game.get_turn() == player:
                return -sys.maxsize
            else:
                return sys.maxsize

        if move in AVOIDED_CASE:
            if game.get_turn() == player:
                return sys.maxsize
            else:
                return -sys.maxsize

        other = self.get_other(player)

        if not any(map(lambda x: x == player, np.array(game.get_board()).flatten())):
            return -sys.maxsize

        if not any(map(lambda x: x == other, np.array(game.get_board()).flatten())):
            return sys.maxsize

        mobility_value = len(game.get_possible_move())
        border_piece = self.get_border_value(game, player)
        stable_piece = self.get_stable_piece(game, player)

        result = mobility_value + 1 / (1 + border_piece) + stable_piece * 4

        return result

    def alpha_beta(
        self,
        depth: int,
        game: othello.OthelloGame,
        alpha: int,
        beta: int,
        player: str,
        move: tuple[int, int] = None,
        turn_number: int = 0,
    ) -> tuple[int, tuple[int, int]]:
        if move is not None:
            game.move(move[0], move[1])

        if depth > MAX_DEPTH:
            return (self.evaluate(game, move, player, turn_number), move)

        new_depth = depth + 1
        return_move = None

        is_maximising = depth % 2 == 0
        best_value = -sys.maxsize if is_maximising else sys.maxsize

        for move in game.get_possible_move():
            result, _ = self.alpha_beta(
                new_depth,
                game.copy_game(),
                alpha,
                beta,
                player,
                move,
                turn_number=turn_number + 1,
            )

            if is_maximising:
                if best_value < result:
                    return_move = move
                    best_value = result
                if beta <= best_value:
                    return (best_value, return_move)
                alpha = max(alpha, best_value)
            else:
                if best_value > result:
                    return_move = move
                    best_value = result
                if alpha >= best_value:
                    return (best_value, return_move)
                beta = min(beta, best_value)
        return (best_value, return_move)

    def update_turn(slef, turn):
        if turn == othello.BLACK:
            return othello.WHITE
        else:
            return othello.BLACK

    def __str__(self):
        return "Da_Silva_Marti_Ruhoff"
