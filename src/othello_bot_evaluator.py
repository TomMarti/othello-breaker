import time

import numpy as np
from ai.Random import Random
import othello


class OthelloBotEvaluator:
    def __init__(self, ais: list):
        self.ais = ais
        self.results = {}
        self.random_ai = Random()

    def evaluate(
        self,
        number_of_games: int = 100,
        board_size: tuple[int, int] = (8, 8),
    ) -> dict:
        metrics = {}
        for ai in self.ais:
            ai_metrics = {
                "wins": 0,
                "losses": 0,
                "draws": 0,
                "invalid_moves": 0,
                "avg_score_difference": [],
                "game_lengths": [],
                "moves_per_game": [],
                "corner_captures": [],
                "move_times": [],
                "total_pieces": [],
            }

            for ai_color in [othello.BLACK, othello.WHITE]:
                opponent_color = (
                    othello.WHITE if ai_color == othello.BLACK else othello.BLACK
                )

                for _ in range(number_of_games // 2):
                    game = othello.OthelloGame(board_size[0], board_size[1], ai_color)
                    moves_count = 0
                    games_moves = []

                    while not game.is_game_over():
                        if game.get_turn() == ai_color:
                            try:
                                start_time = time.time()
                                move = ai.next_move(game.copy_game())
                                ai_metrics["move_times"].append(
                                    time.time() - start_time
                                )

                                if move:
                                    game.move(move[0], move[1])
                                    moves_count += 1
                                    games_moves.append(move)

                                    if move in [
                                        (0, 0),
                                        (0, board_size[1] - 1),
                                        (board_size[0] - 1, 0),
                                        (board_size[0] - 1, board_size[1] - 1),
                                    ]:
                                        ai_metrics["corner_captures"].append(1)
                                    else:
                                        ai_metrics["corner_captures"].append(0)
                            except (
                                othello.InvalidMoveException,
                                othello.InvalidTypeException,
                            ):
                                ai_metrics["invalid_moves"] += 1
                                break
                        else:
                            try:
                                move = self.random_ai.next_move(game.copy_game())
                                if move:
                                    game.move(move[0], move[1])
                                    moves_count += 1
                            except (
                                othello.InvalidMoveException,
                                othello.InvalidTypeException,
                            ):
                                continue

                    ai_score = game.get_scores(ai_color)
                    opponent_score = game.get_scores(opponent_color)

                    if ai_score > opponent_score:
                        ai_metrics["wins"] += 1
                    elif ai_score < opponent_score:
                        ai_metrics["losses"] += 1
                    else:
                        ai_metrics["draws"] += 1

                    ai_metrics["avg_score_difference"].append(ai_score - opponent_score)
                    ai_metrics["game_lengths"].append(moves_count)
                    ai_metrics["moves_per_game"].append(len(games_moves))
                    ai_metrics["total_pieces"].append(ai_score)

            total_games = number_of_games
            metrics[ai.__class__.__name__] = {
                "win_rate": ai_metrics["wins"] / total_games,
                "draw_rate": ai_metrics["draws"] / total_games,
                "loss_rate": ai_metrics["losses"] / total_games,
                "invalid_move_rate": ai_metrics["invalid_moves"] / total_games,
                "avg_score_difference": np.mean(ai_metrics["avg_score_difference"]),
                "avg_game_length": np.mean(ai_metrics["game_lengths"]),
                "avg_moves_per_game": np.mean(ai_metrics["moves_per_game"]),
                "corner_capture_rate": np.mean(ai_metrics["corner_captures"]),
                "avg_move_time": np.mean(ai_metrics["move_times"]),
                "avg_pieces_per_game": np.mean(ai_metrics["total_pieces"]),
                "total_games_played": total_games,
            }

        self.results = metrics
        return metrics

    def print_results(self) -> None:
        for ai_name, metrics in self.results.items():
            print(f"\n=== Results for {ai_name} vs Random ===")
            print(f"Total games played: {metrics['total_games_played']}")
            print(f"\nPerformance Metrics:")
            print(f"Win rate: {metrics['win_rate']:.2%}")
            print(f"Draw rate: {metrics['draw_rate']:.2%}")
            print(f"Loss rate: {metrics['loss_rate']:.2%}")
            print(f"Invalid move rate: {metrics['invalid_move_rate']:.2%}")

            print(f"\nGame Statistics:")
            print(f"Average score difference: {metrics['avg_score_difference']:.2f}")
            print(f"Average pieces per game: {metrics['avg_pieces_per_game']:.2f}")
            print(f"Average game length: {metrics['avg_game_length']:.2f}")
            print(f"Average moves per game: {metrics['avg_moves_per_game']:.2f}")

            print(f"\nStrategy Metrics:")
            print(f"Corner capture rate: {metrics['corner_capture_rate']:.2%}")
            print(f"Average move time: {metrics['avg_move_time']:.4f} seconds")


if __name__ == "__main__":
    evaluator = OthelloBotEvaluator([Random()])
    evaluator.evaluate()
    evaluator.print_results()
