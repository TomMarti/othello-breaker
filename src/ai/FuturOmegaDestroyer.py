''' Example of a random AI. The class name has to be the same as the module name.
'''

from __future__ import annotations # postpones the evaluation of the type hints, hence they do not need to be imported
import random
import othello


class FuturOmegaDestroyer:
    '''The name of this class must be the same as its file.
    
    '''

    def __init__(self):
        pass

    def next_move(self, board: othello.OthelloGame) -> tuple[int, int]:
        """Returns the next move to play.

        Args:
            board (othello.OthelloGame): _description_

        Returns:
            tuple[int, int]: the next move (for instance: (2, 3) for (row, column), starting from 0)
        """

        legal_moves = board.get_possible_move()

        best_move = None
        best_move_value = None
        for move in legal_moves:
            move_value = self.move_value(board, move)
            if best_move is None or best_move_value < move_value:
                best_move = move
                best_move_value = move_value

        return best_move
    
    def move_value(self, board: othello.OthelloGame, move: tuple[int, int]) -> int:
        """
        Evaluate the move value by exploring only necessary case
        """

        work_board = board.get_board()
        current_player = board.turn
        opponent = 'W'
        if current_player == 'W':
            opponent = 'B'

        value = 0 # The placed piece is not counted, change to one for that

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
                    elif color_next_case == '.':
                        break
                except IndexError:
                    # Out of bound, no gain
                    break

        return value
    
    def next_direction_to_check(self, counter):
        """
        Utility method for move_value() function, private use
        """
        moves = {
            0: (0, 1),
            1: (1, 1),
            2: (1, 0),
            3: (1, -1),
            4: (0, -1),
            5: (-1, -1),
            6: (-1, 0),
            7: (-1, 1)
        }

        if counter not in moves:
            raise IndexError('Illegal Counter')
            
        direction = moves[counter]
        return direction[0], direction[1]


    def __str__(self):
        return "FuturOmegaDestroyer"