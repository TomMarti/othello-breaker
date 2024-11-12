import numpy as np
import othello


class OthelloEvaluator:
    def __init__(self):
        # Game phase boundaries based on disc count
        self.EARLY_GAME = 20
        self.MID_GAME = 40
        self.LATE_GAME = 64  # Full board

        # Pre-computed pattern weights for different game phases
        # These would normally be learned from game data
        self.pattern_weights = {
            "early": np.array([0.2, 0.4, 0.4]),  # Mobility, Stability, Corner patterns
            "mid": np.array([0.3, 0.4, 0.3]),
            "late": np.array([0.1, 0.5, 0.4]),
        }

        # Initialize pattern tables and indices
        self._init_patterns()

    def _init_patterns(self):
        """Initialize pattern recognition tables"""
        # Corner patterns (2x2 squares at each corner)
        self.corner_patterns = [
            [(0, 0), (0, 1), (1, 0), (1, 1)],  # Top-left
            [(0, 6), (0, 7), (1, 6), (1, 7)],  # Top-right
            [(6, 0), (6, 1), (7, 0), (7, 1)],  # Bottom-left
            [(6, 6), (6, 7), (7, 6), (7, 7)],  # Bottom-right
        ]

        # Edge patterns (horizontal and vertical lines)
        self.edge_patterns = {
            "horizontal": [(i, j) for i in [0, 7] for j in range(8)],
            "vertical": [(i, j) for j in [0, 7] for i in range(8)],
        }

    def _count_mobility(self, board, player):
        """
        Calculate mobility score (number of legal moves)
        Returns approximate mobility using line-based calculation
        """
        mobility = 0
        opponent = -player

        # Check horizontally and vertically for potential moves
        directions = [(0, 1), (1, 0), (1, 1), (-1, 1)]

        for i in range(8):
            for j in range(8):
                if board[i][j] == 0:  # Empty square
                    for di, dj in directions:
                        # Check if move would flip opponent's pieces
                        if self._would_flip(board, i, j, di, dj, player):
                            mobility += 1
                            break

        return mobility

    def _would_flip(self, board, i, j, di, dj, player):
        """Helper function to check if a move would flip opponent's pieces"""
        opponent = -player
        current_i, current_j = i + di, j + dj

        # First adjacent must be opponent's piece
        if not (0 <= current_i < 8 and 0 <= current_j < 8):
            return False
        if board[current_i][current_j] != opponent:
            return False

        # Look for player's piece to sandwich opponent's pieces
        current_i, current_j = current_i + di, current_j + dj
        while 0 <= current_i < 8 and 0 <= current_j < 8:
            if board[current_i][current_j] == 0:
                return False
            if board[current_i][current_j] == player:
                return True
            current_i, current_j = current_i + di, current_j + dj

        return False

    def _evaluate_patterns(self, board, player):
        """
        Evaluate position based on important patterns:
        - Corner occupation and stability
        - Edge control
        - Overall disc formation
        """
        pattern_score = 0

        # Evaluate corners (highest value)
        for corner in self.corner_patterns:
            corner_val = sum(board[i][j] == player for i, j in corner)
            pattern_score += corner_val * 10  # Corners are very valuable

        # Evaluate edges
        for edge_squares in self.edge_patterns.values():
            edge_val = sum(board[i][j] == player for i, j in edge_squares)
            pattern_score += edge_val * 5  # Edges are valuable but less than corners

        return pattern_score

    def _get_game_phase(self, board):
        """Determine game phase based on number of discs"""
        disc_count = np.sum(np.abs(board))

        if disc_count <= self.EARLY_GAME:
            return "early"
        elif disc_count <= self.MID_GAME:
            return "mid"
        else:
            return "late"

    def convert_board(self, board):
        """Convert board to numpy array"""
        nboard = []
        for row in board:
            nrow = []
            for cell in row:
                if cell == othello.BLACK:
                    nrow.append(1)
                elif cell == othello.WHITE:
                    nrow.append(-1)
                else:
                    nrow.append(0)
            nboard.append(nrow)
        print(nboard)
        return np.array(nboard)

    def evaluate(self, board, player):
        """
        Main evaluation function that combines:
        - Mobility (current and potential)
        - Pattern-based evaluation
        - Game phase specific weights

        Returns a score from player's perspective
        Positive score means player is winning, negative means opponent is winning
        """
        # Convert board to numpy array if needed
        board = self.convert_board(board)
        player = 1 if player == "B" else -1

        # Get game phase
        phase = self._get_game_phase(board)

        # Calculate components
        mobility_score = self._count_mobility(board, player)
        pattern_score = self._evaluate_patterns(board, player)

        # Calculate material (disc count) advantage
        material_score = np.sum(board == player) - np.sum(board == -player)

        # Combine scores using phase-specific weights
        weights = self.pattern_weights[phase]
        final_score = (
            weights[0] * mobility_score
            + weights[1] * pattern_score
            + weights[2] * material_score
        )

        return final_score


# Example usage
if __name__ == "__main__":
    # Example board (0=empty, 1=player, -1=opponent)
    board = [
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", "B", ".", ".", ".", "."],
        [".", ".", "B", "B", "B", ".", ".", "."],
        [".", ".", ".", "B", "W", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
    ]

    evaluator = OthelloEvaluator()
    score = evaluator.evaluate(board, "B")
    print(f"Position evaluation: {score}")
