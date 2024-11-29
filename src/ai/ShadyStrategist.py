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

CORNER_DIAG = {
    (0, 0): (1, 1),
    (8, 0): (-1, 1),
    (0, 6): (1, -1),
    (8, 6): (-1, -1),
}

CACHE = {}


class ShadyStrategist:
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

    def current_stat_to_string(self, board, move, turn) -> str:
        string = ""
        for x in np.array(board).flatten():
            string += x
        return string + str(move) + turn

    def get_border_value(self, game: othello.OthelloGame, player: str):
        value = 0
        board = game.get_board()
        for y in range(len(board)):
            for x in range(len(board[y])):
                if board[y][x] == player:
                    value += self.is_border(x, y, board)

        return value

    def get_other(self, player_turn: str) -> str:
        return othello.BLACK if player_turn == othello.WHITE else othello.WHITE

    def get_stable_piece(self, game: othello.OthelloGame, player: str):

        board = game.get_board()
        board_len = len(board)
        stable = np.full((board_len, len(board[-1])), False, dtype=bool)

        for corner_cell in CORNER:
            if board[corner_cell[1]][corner_cell[0]] == player:
                stable[corner_cell[1]][corner_cell[0]] = True
                for dir in CORNER_DIRECTION[corner_cell]:
                    x = corner_cell[0] + dir[0]
                    y = corner_cell[1] + dir[1]
                    while board[y][x] == player:
                        stable[y][x] = True
                        x += dir[0]
                        y += dir[1]
                        if not (0 <= y < len(board)) or not (0 <= x < len(board[y])):
                            break

        for y in range(len(board)):
            for x in range(len(board[y])):
                if board[y][x] == player:
                    stable_hor = True
                    stable_ver = True
                    stable_diag = True

                    if x > 0:
                        if stable[y][x - 1]:
                            stable_hor = True
                    else:
                        stable_hor = True

                    if x < len(stable[y]) - 1:
                        if stable[y][x + 1]:
                            stable_hor = True

                    if y > 0:
                        if stable[y - 1][x]:
                            stable_ver = True
                    else:
                        stable_ver = True

                    if y < len(stable) - 1:
                        if stable[y + 1][x]:
                            stable_ver = True
                    else:
                        stable_ver = True

                    if y > 0 and x > 0:
                        if stable[y - 1][x - 1]:
                            stable_diag = True
                    else:
                        stable_diag = True

                    if y < len(stable) - 1 and x < len(stable[y]) - 1:
                        if stable[y + 1][x]:
                            stable_diag = True
                    else:
                        stable_diag = True

                    if stable_diag and stable_hor and stable_ver:
                        stable[y][x] = True

        return np.count_nonzero(stable)

    def next_move(self, board: othello.OthelloGame) -> tuple[int, int]:
        """Returns the next move to play.

        Args:
            board (othello.OthelloGame): _description_

        Returns:
            tuple[int, int]: the next move (for instance: (2, 3) for (row, column), starting from 0)
        """

        player = board.get_turn()
        possible_moves = set(board.get_possible_move())
        print(f"Shady Strategist : {possible_moves}")
        if len(possible_moves) > 1:
            _, move = self.alpha_beta(
                0,
                board.copy_game(),
                -sys.maxsize,
                sys.maxsize,
                player,
            )
            return move
        else:
            return board.get_possible_move()[0]

    def evaluate(
        self, game: othello.OthelloGame, move, player_move, player, turn_number=0
    ) -> float:

        current_state_hash = self.current_stat_to_string(
            game.get_board(), move, player_move
        )

        if current_state_hash in CACHE:
            return CACHE[current_state_hash]

        if game.get_turn() == player:
            mobility_value = -len(set(game.get_possible_move()))
        else:
            mobility_value = len(set(game.get_possible_move()))

        # border_piece = self.get_border_value(game, player)
        stable_piece = self.get_stable_piece(game, player)
        # if turn_number < 7:
        #     value = mobility_value * 20 + 1 / (1 + border_piece) + stable_piece * 10
        # else:
        value = (
            stable_piece * 2 - mobility_value
        )  # mobility_value + 1 / (1 + border_piece) +

        CACHE[current_state_hash] = value
        return value

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
            player_move = game.get_turn()
            game.move(move[0], move[1])

        if depth > MAX_DEPTH:
            return (
                self.evaluate(game, move, player_move, player, turn_number),
                move,
            )

        if game.is_game_over():
            if game.return_winner() == player:
                return sys.maxsize, move
            else:
                return -sys.maxsize, move

        new_depth = depth + 1
        return_move = None

        is_maximising = game.get_turn() == player
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
        return "ShadyStrategist "
