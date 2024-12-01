import time
import numpy as np
from ai.Random import Random
from ai.Strategist import Strategist
import othello


class OthelloBotEvaluator:
    def __init__(self, ais: list):
        self.ais = ais
        self.results = {}

    def evaluate(
        self,
        random_ai: Random,
        number_of_games: int = 100,
        board_size: tuple[int, int] = (8, 8),
    ) -> dict:
        random_metrics = {
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
            "opponents": [],  # Track performance against each opponent
        }

        total_games = 0
        for opponent_ai in self.ais:
            opponent_name = opponent_ai.__class__.__name__
            opponent_metrics = {"wins": 0, "losses": 0, "draws": 0}

            for random_color in [othello.BLACK, othello.WHITE]:
                opponent_color = (
                    othello.WHITE if random_color == othello.BLACK else othello.BLACK
                )

                for _ in range(number_of_games // 2):
                    game = othello.OthelloGame(
                        board_size[0], board_size[1], random_color
                    )
                    moves_count = 0
                    random_moves = []

                    while not game.is_game_over():
                        if game.get_turn() == random_color:
                            try:
                                start_time = time.time()
                                move = random_ai.next_move(game.copy_game())
                                random_metrics["move_times"].append(
                                    time.time() - start_time
                                )

                                if move:
                                    game.move(move[0], move[1])
                                    moves_count += 1
                                    random_moves.append(move)

                                    if move in [
                                        (0, 0),
                                        (0, board_size[1] - 1),
                                        (board_size[0] - 1, 0),
                                        (board_size[0] - 1, board_size[1] - 1),
                                    ]:
                                        random_metrics["corner_captures"].append(1)
                                    else:
                                        random_metrics["corner_captures"].append(0)
                            except (
                                othello.InvalidMoveException,
                                othello.InvalidTypeException,
                            ):
                                random_metrics["invalid_moves"] += 1
                                break
                        else:
                            try:
                                move = opponent_ai.next_move(game.copy_game())
                                if move:
                                    game.move(move[0], move[1])
                                    moves_count += 1
                            except (
                                othello.InvalidMoveException,
                                othello.InvalidTypeException,
                            ):
                                continue

                    random_score = game.get_scores(random_color)
                    opponent_score = game.get_scores(opponent_color)

                    if random_score > opponent_score:
                        random_metrics["wins"] += 1
                        opponent_metrics["losses"] += 1
                    elif random_score < opponent_score:
                        random_metrics["losses"] += 1
                        opponent_metrics["wins"] += 1
                    else:
                        random_metrics["draws"] += 1
                        opponent_metrics["draws"] += 1

                    random_metrics["avg_score_difference"].append(
                        random_score - opponent_score
                    )
                    random_metrics["game_lengths"].append(moves_count)
                    random_metrics["moves_per_game"].append(len(random_moves))
                    random_metrics["total_pieces"].append(random_score)
                    total_games += 1

            # Store per-opponent metrics
            random_metrics["opponents"].append(
                {"name": opponent_name, "metrics": opponent_metrics}
            )

        # Calculate final metrics
        self.results["Random"] = {
            "win_rate": random_metrics["wins"] / total_games,
            "draw_rate": random_metrics["draws"] / total_games,
            "loss_rate": random_metrics["losses"] / total_games,
            "invalid_move_rate": random_metrics["invalid_moves"] / total_games,
            "avg_score_difference": np.mean(random_metrics["avg_score_difference"]),
            "avg_game_length": np.mean(random_metrics["game_lengths"]),
            "avg_moves_per_game": np.mean(random_metrics["moves_per_game"]),
            "corner_capture_rate": np.mean(random_metrics["corner_captures"]),
            "avg_move_time": np.mean(random_metrics["move_times"]),
            "avg_pieces_per_game": np.mean(random_metrics["total_pieces"]),
            "total_games_played": total_games,
            "per_opponent_results": random_metrics["opponents"],
        }

        return self.results

    def print_results(self) -> None:
        metrics = self.results["Random"]
        print("\n=== Results for Random AI ===")
        print(f"Total games played: {metrics['total_games_played']}")

        print("\nOverall Performance Metrics:")
        print(f"Win rate: {metrics['win_rate']:.2%}")
        print(f"Draw rate: {metrics['draw_rate']:.2%}")
        print(f"Loss rate: {metrics['loss_rate']:.2%}")
        print(f"Invalid move rate: {metrics['invalid_move_rate']:.2%}")

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


if __name__ == "__main__":
    evaluator = OthelloBotEvaluator([Random(), Strategist()])
    random_ai = Random()
    evaluator.evaluate(random_ai)
    evaluator.print_results()
