import time
from ai.Marti_Da_Silva_Ruhoff import Marti_Da_Silva_Ruhoff
from ai.MaximumStoneStrategy import MaximumStoneStrategy
from ai.MaximumStoneStrategyOptimized import MaximumStoneStrategyOptimized
from ai.Random import Random
from ai.Strategist import Strategist
import othello


class OthelloBotEvaluator:
    def __init__(self, ais: list):
        self.ais = ais
        self.results = {
            "total_games_played": 0,
            "win_rate": 0.0,
            "draw_rate": 0.0,
            "loss_rate": 0.0,
            "invalid_move_rate": 0.0,
            "avg_score_difference": 0.0,
            "avg_pieces_per_game": 0.0,
            "avg_game_length": 0.0,
            "avg_moves_per_game": 0.0,
            "corner_capture_rate": 0.0,
            "avg_move_time": 0.0,
            "skipped_turns_rate": 0.0,
            "per_opponent_results": [],
        }

    def play_game(
        self,
        evaluated_ai,
        opponent_ai,
        board_size: tuple[int, int] = (7, 9),
        evaluated_color: str = othello.BLACK,
        opponent_color: str = othello.WHITE,
    ) -> dict[str, any]:
        """
        Play a single game between two AIs and return the results

        Returns:
            Dictionary containing game results and statistics of a game
        """
        game = othello.OthelloGame(board_size[0], board_size[1], othello.BLACK)
        moves_count = 0
        invalid_moves = 0
        corners_captured = 0
        total_move_time = 0
        skipped_turns = 0

        corners = [
            (0, 0),
            (0, board_size[1] - 1),
            (board_size[0] - 1, 0),
            (board_size[0] - 1, board_size[1] - 1),
        ]

        while not game.is_game_over():
            current_player = game.get_turn()
            current_ai = (
                evaluated_ai if current_player == evaluated_color else opponent_ai
            )

            possible_moves = game.get_possible_move()

            if not possible_moves:
                skipped_turns += 1
                game.switch_turn()
                continue

            start_time = time.time()
            try:
                move = current_ai.next_move(game.copy_game())
                move_time = time.time() - start_time
                total_move_time += move_time

                if move in corners:
                    corners_captured += 1

                game.move(move[0], move[1])
                moves_count += 1

            except (othello.InvalidMoveException, othello.InvalidTypeException):
                invalid_moves += 1
                game.switch_turn()

        black_score, white_score = game.get_scores()
        evaluated_score = (
            black_score if evaluated_color == othello.BLACK else white_score
        )
        opponent_score = (
            white_score if evaluated_color == othello.BLACK else black_score
        )

        winner = game.return_winner()

        return {
            "winner": winner,
            "moves_count": moves_count,
            "scores": (evaluated_score, opponent_score),
            "invalid_moves": invalid_moves,
            "corners_captured": corners_captured,
            "avg_move_time": total_move_time / max(moves_count, 1),
            "total_pieces": evaluated_score + opponent_score,
            "skipped_turns": skipped_turns,
        }

    def evaluate(
        self,
        evaluated_ai,
        number_of_games: int = 100,
        board_size: tuple[int, int] = (7, 9),
    ) -> dict[str, any]:
        """
        Evaluate an AI by playing multiple games against different opponents
        """
        print(f"Evaluating {str(evaluated_ai)}...")
        total_games = 0
        total_wins = 0
        total_draws = 0
        total_losses = 0
        total_invalid_moves = 0
        total_score_diff = 0
        total_pieces = 0
        total_moves = 0
        total_corners_captured = 0
        total_move_time = 0
        total_skipped_turns = 0

        per_opponent_results = []

        for opponent_ai in self.ais:
            print(f"Playing against {str(opponent_ai)}...")
            opponent_stats = {
                "name": str(opponent_ai),
                "metrics": {
                    "wins": 0,
                    "losses": 0,
                    "draws": 0,
                    "invalid_moves": 0,
                    "avg_score_diff": 0,
                    "avg_move_time": 0,
                    "skipped_turns": 0,
                },
            }

            for i in range(number_of_games):
                print(f"Game {i+1}/{number_of_games}")
                evaluated_color = othello.BLACK if i % 2 == 0 else othello.WHITE
                opponent_color = (
                    othello.WHITE if evaluated_color == othello.BLACK else othello.BLACK
                )

                result = self.play_game(
                    evaluated_ai,
                    opponent_ai,
                    board_size,
                    evaluated_color,
                    opponent_color,
                )

                total_games += 1
                total_invalid_moves += result["invalid_moves"]
                total_pieces += result["total_pieces"]
                total_moves += result["moves_count"]
                total_corners_captured += result["corners_captured"]
                total_move_time += result["avg_move_time"]
                total_skipped_turns += result["skipped_turns"]

                score_diff = result["scores"][0] - result["scores"][1]
                total_score_diff += score_diff

                opponent_stats["metrics"]["skipped_turns"] += result["skipped_turns"]

                if result["winner"] == evaluated_color:
                    total_wins += 1
                    opponent_stats["metrics"]["wins"] += 1
                elif result["winner"] == opponent_color:
                    total_losses += 1
                    opponent_stats["metrics"]["losses"] += 1
                else:
                    total_draws += 1
                    opponent_stats["metrics"]["draws"] += 1

            per_opponent_results.append(opponent_stats)

        self.results = {
            "total_games_played": total_games,
            "win_rate": total_wins / total_games,
            "draw_rate": total_draws / total_games,
            "loss_rate": total_losses / total_games,
            "invalid_move_rate": total_invalid_moves / total_games,
            "avg_score_difference": total_score_diff / total_games,
            "avg_pieces_per_game": total_pieces / total_games,
            "avg_game_length": total_moves / total_games,
            "avg_moves_per_game": total_moves / total_games,
            "corner_capture_rate": total_corners_captured / (4 * total_games),
            "avg_move_time": total_move_time / total_games,
            "skipped_turns_rate": total_skipped_turns / total_games,
            "per_opponent_results": per_opponent_results,
        }

        return self.results

    def print_results(self) -> None:
        metrics = self.results
        print("\n=== Results for AI ===")
        print(f"Total games played: {metrics['total_games_played']}")

        print("\nOverall Performance Metrics:")
        print(f"Win rate: {metrics['win_rate']:.2%}")
        print(f"Draw rate: {metrics['draw_rate']:.2%}")
        print(f"Loss rate: {metrics['loss_rate']:.2%}")
        print(f"Invalid move rate: {metrics['invalid_move_rate']:.2%}")
        print(f"Skipped turns per game: {metrics['skipped_turns_rate']:.2f}")

        print("\nGame Statistics:")
        print(f"Average score difference: {metrics['avg_score_difference']:.2f}")
        print(f"Average pieces per game: {metrics['avg_pieces_per_game']:.2f}")
        print(f"Average game length: {metrics['avg_game_length']:.2f}")
        print(f"Average moves per game: {metrics['avg_moves_per_game']:.2f}")

        print("\nStrategy Metrics:")
        print(f"Corner capture rate: {metrics['corner_capture_rate']:.2%}")
        print(f"Average move time: {metrics['avg_move_time']:.4f} seconds")

        print("\nPer-Opponent Results:")
        for opponent in metrics["per_opponent_results"]:
            name = opponent["name"]
            opp_metrics = opponent["metrics"]
            total_games = (
                opp_metrics["wins"] + opp_metrics["losses"] + opp_metrics["draws"]
            )
            print(f"\nVs {name}:")
            print(f"Win rate: {opp_metrics['wins']/total_games:.2%}")
            print(f"Draw rate: {opp_metrics['draws']/total_games:.2%}")
            print(f"Loss rate: {opp_metrics['losses']/total_games:.2%}")
            print(
                f"Average skipped turns: {opp_metrics['skipped_turns']/total_games:.2f}"
            )


if __name__ == "__main__":
    evaluator = OthelloBotEvaluator(
        [
            Random(),
            MaximumStoneStrategy(),
            MaximumStoneStrategyOptimized(),
            Strategist(),
        ]
    )

    ai = Marti_Da_Silva_Ruhoff()
    evaluator.evaluate(ai, 2)
    evaluator.print_results()
