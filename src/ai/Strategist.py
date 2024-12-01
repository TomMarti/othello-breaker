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


class Strategist:
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

    def current_state_to_string(self, board, move, turn) -> str:
        return "".join(sum(board, []) + [str(move), turn])

    def get_border_value(self, game: othello.OthelloGame, player: str):
        value = 0
        board = game.get_board()
        for y in range(len(board)):
            for x in range(len(board[y])):
                if board[y][x] == player:
                    value += self.is_border(x, y, board)

        return value

    def get_other(self, player_turn: str) -> str:
        """
        TODO: If not used in final version, remove it
        """
        return othello.BLACK if player_turn == othello.WHITE else othello.WHITE

    def get_stable_piece(
        self, game: othello.OthelloGame, player: str
    ) -> tuple[(int, int)]:
        other = self.update_turn(player)
        board = game.get_board()
        board_len = len(board)
        stable_player = np.full((board_len, len(board[-1])), False, dtype=bool)
        stable_other = np.full((board_len, len(board[-1])), False, dtype=bool)

        for corner_cell in CORNER:
            if board[corner_cell[1]][corner_cell[0]] == player:
                stable_player[corner_cell[1]][corner_cell[0]] = True
                for dir in CORNER_DIRECTION[corner_cell]:
                    x = corner_cell[0] + dir[0]
                    y = corner_cell[1] + dir[1]
                    while board[y][x] == player:
                        stable_player[y][x] = True
                        x += dir[0]
                        y += dir[1]
                        if not (0 <= y < len(board)) or not (0 <= x < len(board[y])):
                            break
            if board[corner_cell[1]][corner_cell[0]] == other:
                stable_other[corner_cell[1]][corner_cell[0]] = True
                for dir in CORNER_DIRECTION[corner_cell]:
                    x = corner_cell[0] + dir[0]
                    y = corner_cell[1] + dir[1]
                    while board[y][x] == other:
                        stable_other[y][x] = True
                        x += dir[0]
                        y += dir[1]
                        if not (0 <= y < len(board)) or not (0 <= x < len(board[y])):
                            break

        for y in range(len(board)):
            for x in range(len(board[y])):
                if board[y][x] is not othello.NONE:
                    if board[y][x] == player:
                        stable = stable_player
                    else:
                        stable = stable_other

                    stable_hor = False
                    stable_ver = False
                    stable_diag = False

                    if x > 0:
                        if stable[y][x - 1]:
                            stable_hor = True
                    else:
                        stable_hor = True

                    if x < len(stable[y]) - 1:
                        if stable[y][x + 1]:
                            stable_hor = True
                    else:
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

        return np.count_nonzero(stable_player), np.count_nonzero(stable_other)

    def next_move(self, board: othello.OthelloGame) -> tuple[int, int]:
        """Returns the next move to play.

        Args:
            board (othello.OthelloGame): _description_

        Returns:
            tuple[int, int]: the next move (for instance: (2, 3) for (row, column), starting from 0)
        """

        player = board.get_turn()
        possible_moves = set(board.get_possible_move())
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
        current_state_hash = self.current_state_to_string(
            game.get_board(), move, player_move
        )

        if current_state_hash in CACHE:
            return CACHE[current_state_hash]

        value, _ = self.get_stable_piece(game, player)

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
    ) -> tuple[int, tuple[int, int]]:
        if move is not None:
            player_move = game.get_turn()
            game.move(move[0], move[1])

        if depth > MAX_DEPTH:
            return (
                self.evaluate(game, move, player_move, player),
                move,
            )

        if game.is_game_over():
            if game.return_winner() == player:
                return sys.maxsize, move
            else:
                return -sys.maxsize, move

        new_depth = depth + 1

        legal_moves = game.get_possible_move()
        return_move = legal_moves[0]

        is_maximising = game.get_turn() == player
        best_value = -sys.maxsize if is_maximising else sys.maxsize
        for move in game.get_possible_move():
            result, _ = self.alpha_beta(
                new_depth, game.copy_game(), alpha, beta, player, move
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
        return "Strategist"
