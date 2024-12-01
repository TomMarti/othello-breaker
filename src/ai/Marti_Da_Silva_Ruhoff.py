"""Example of a random AI. The class name has to be the same as the module name."""

from __future__ import (
    annotations,
)  # postpones the evaluation of the type hints, hence they do not need to be imported
import othello
import sys
import numpy as np

MAX_DEPTH = 5
CORNER = [(0, 0), (8, 0), (0, 6), (8, 6)]

CORNER_DIRECTION = {
    (0, 0): [(1, 0), (0, 1)],
    (8, 0): [(-1, 0), (0, 1)],
    (0, 6): [(1, 0), (0, -1)],
    (8, 6): [(-1, 0), (0, -1)],
}

CACHE = {}


class Marti_Da_Silva_Ruhoff:
    """The name of this class must be the same as its file."""

    def __init__(self):
        pass

    def current_stat_to_string(self, board) -> str:
        """
        Function used to create a hash for the cache
        """
        return np.array2string(np.array(board))

    def get_other_player(self, player_turn: str) -> str:
        """
        Return the other player than the one given
        """
        return othello.BLACK if player_turn == othello.WHITE else othello.WHITE

    def get_stable_piece(
        self, game: othello.OthelloGame, player: str
    ) -> tuple[(int, int)]:
        """
        Return the count of stable piece for the player and his opponent.
        A stable piece is a piece that cannot be flipped anymore.
        """

        other = self.get_other_player(player)
        board = game.get_board()

        # Genereate a mask for both player of their stable piece
        stable_player = np.full(
            (game.get_rows(), game.get_columns()), False, dtype=bool
        )
        stable_other = np.full((game.get_rows(), game.get_columns()), False, dtype=bool)

        # Check the border to init stable piece
        for corner_cell in CORNER:
            if board[corner_cell[1]][corner_cell[0]] is not None:
                if board[corner_cell[1]][corner_cell[0]] == player:
                    stable = stable_player
                    target = player
                else:
                    stable = stable_other
                    target = other

                stable[corner_cell[1]][corner_cell[0]] = True
                for dir in CORNER_DIRECTION[corner_cell]:
                    x = corner_cell[0] + dir[0]
                    y = corner_cell[1] + dir[1]
                    while board[y][x] == target:
                        stable[y][x] = True
                        x += dir[0]
                        y += dir[1]
                        if not (0 <= y < len(board)) or not (0 <= x < len(board[y])):
                            break

        # A stable piece is a piece that has one stable piece next to it horizontally, vertically and in his diagonal at the same time.
        for y in range(len(board)):
            for x in range(len(board[y])):
                if board[y][x] is not othello.NONE:
                    if board[y][x] == player:
                        stable = stable_player
                    else:
                        stable = stable_other

                    # Init flag for each direction
                    stable_hor = False
                    stable_ver = False
                    stable_diag = False

                    # Check horizontally
                    if x > 0:
                        if stable[y][x - 1]:
                            stable_hor = True
                    else:
                        stable_hor = True

                    if x < game.get_columns() - 1:
                        if stable[y][x + 1]:
                            stable_hor = True
                    else:
                        stable_hor = True

                    # Check vertically
                    if y > 0:
                        if stable[y - 1][x]:
                            stable_ver = True
                    else:
                        stable_ver = True

                    if y < game.get_rows() - 1:
                        if stable[y + 1][x]:
                            stable_ver = True
                    else:
                        stable_ver = True

                    # Check diagonally
                    if y > 0 and x > 0:
                        if stable[y - 1][x - 1]:
                            stable_diag = True
                    else:
                        stable_diag = True

                    if y < game.get_rows() - 1 and x < game.get_columns() - 1:
                        if stable[y + 1][x]:
                            stable_diag = True
                    else:
                        stable_diag = True

                    # If the piece has one stable piece horizontally, vertically and diagonally at same time, it's stable itself
                    if stable_diag and stable_hor and stable_ver:
                        stable[y][x] = True

        # Count the number of stable piece in the mask
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
        # Check if there is more than one possible move. If not, return the only move possible (optimize time reflexion)
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

    def evaluate(self, game: othello.OthelloGame, player) -> float:
        """
        Function that return a score based on the actual board
        """
        # Check if the board has already been calculated
        current_state_hash = self.current_stat_to_string(game.get_board())

        if current_state_hash in CACHE:
            return CACHE[current_state_hash]

        # Count the mobility for both player
        if game.get_turn() == player:
            own_mobility_value = len(set(game.get_possible_move()))
            game.switch_turn()
            other_mobility_value = len(set(game.get_possible_move()))
        else:
            other_mobility_value = len(set(game.get_possible_move()))
            game.switch_turn()
            own_mobility_value = len(set(game.get_possible_move()))

        own_stable_piece, other_stable_piece = self.get_stable_piece(game, player)

        # The factor for each value have been set by trial
        OWN_STABLE_FACTOR = 5
        OTHER_STABLE_FACTOR = 10
        OWN_MOBILITY_FACTOR = 1
        OTHER_MOBILITY_FACTOR = 2

        value = (
            OWN_STABLE_FACTOR * own_stable_piece
            - OTHER_STABLE_FACTOR * other_stable_piece
            + OWN_MOBILITY_FACTOR * own_mobility_value
            - OTHER_MOBILITY_FACTOR * other_mobility_value
        )

        # set the value in the cache
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
        """
        This is the alpha-beta algorithms
        """
        if move is not None:
            game.move(move[0], move[1])

        if depth > MAX_DEPTH:
            return (
                self.evaluate(game, player),
                move,
            )

        # Check if the game is winned by a player and return the corresponding value
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

        # check all the moves
        for move in legal_moves:
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

    def __str__(self):
        return "Marti_Da_Silva_Ruhoff "
