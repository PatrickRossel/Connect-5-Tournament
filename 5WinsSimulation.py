"""This script simulates all possible matches and collects the results

You may change anything you want. If you have any questions: yfrank@students.uni-mainz.de
(18.09.22)
"""
import os
from collections import defaultdict
from dataclasses import dataclass
from itertools import combinations

from typing import List, Dict, Tuple


def get_groups() -> Dict[str, str]:
    """
    Reads participants from file

    :return: mapping of group name to execution command
    """
    groups: Dict[str, str] = dict()
    with open('groups.txt', 'r') as group_file:
        for line in group_file.readlines():
            team, program = line.split(';')
            program = program.replace('\n', '')
            groups[team] = program
    return groups


# Class to collect result of match in
@dataclass
class GameResult:
    player_A: str
    player_B: str
    winner: str
    # Its easier to use this as string
    number_of_moves: str
    is_draw: bool = False


def get_results() -> Tuple[str, str]:
    """
    Function to retrieve data from files

    :return: Pair of winner and number of moves
    """
    with open('Win.txt', 'r') as win_file:
        winner = win_file.readline().replace('\n', '')
    with open('5GewinntState.txt', 'r') as state_file:
        moves = state_file.readline().split()[1].replace('\n', '')
    return winner, moves


def simulate_games(groups: Dict[str, str], silent: bool = True) -> List[GameResult]:
    """
    Function which simulates the games for the given groups

    :param groups: Mapping of group name to execution command
    :param silent: Flag to hide output of match and only print results

    :return: List containing all results
    """
    results: List[GameResult] = []

    def simulate_game(player_A: str, player_B: str):
        """
        Internal function which simulates a game.

        :param player_A: Player which should be red
        :param player_B: Player which should be yellow
        """
        print(f"{player_A} vs. {player_B}")
        # Simulate game
        os.system(f'python 5Gewinnt.py "{groups[player_A]}" "{groups[player_B]}" {" > dump.txt" if silent else ""}')
        winner, moves = get_results()
        # Collect result
        results.append(GameResult(player_A,
                                  player_B,
                                  player_A if winner == 'A' else player_B,
                                  moves, is_draw=winner == "Draw")
                       )
        # Output for progress
        if winner == "Draw":
            print("Draw")
        else:
            print(f"Winner: {player_A if winner == 'A' else player_B} after {moves} moves")

    # Simulate games for pair
    for left, right in combinations(groups.keys(), 2):
        simulate_game(left, right)
        simulate_game(right, left)
    return results



# Class to collect accumulated results of matches for participant
@dataclass
class CombinedResult:
    wins: int = 0
    wins_A: int = 0
    wins_B: int = 0
    draws: int = 0
    draws_A: int = 0
    draws_B: int = 0
    avg_moves: float = 0.0


def save_overall(results: List[GameResult]):
    """
    Function to store accumulated results of team in file

    :param results: List of all game results
    """
    # Default spacings for table
    spacing_wins = 10
    spacing_teams = 7
    spacing_moves = 9
    # Collect results for each team
    overall_results: Dict[str, CombinedResult] = defaultdict(CombinedResult)
    for result in results:
        own = overall_results[result.player_A]
        enemy = overall_results[result.player_B]
        if result.is_draw:
            own.draws_A += 1
            own.draws += 1
            enemy.draws_B += 1
            enemy.draws += 1
        else:
            if result.winner == result.player_A:
                own.wins += 1
                own.wins_A += 1
            else:
                enemy.wins += 1
                enemy.wins_B += 1
        own.avg_moves += float(result.number_of_moves)
        enemy.avg_moves += float(result.number_of_moves)
    # Store in file
    with open("overall.txt", 'w') as overall_file:
        overall_file.write(f"Number of games per team: {(len(overall_results.keys()) - 1) * 2}\n")
        overall_file.write(f"Number of games overall: {len(results)}\n\n")
        # Write header
        overall_file.write(
            "┌─" + ("─" * spacing_teams + "─┬─") + ("─" * spacing_wins + "─┬─") * 6 + "─" * spacing_moves + "─┐\n")
        overall_file.write(
            f"│ {'Team':^{spacing_teams}s} │ {'Wins':^{spacing_wins}s} │ {'Wins as A':^{spacing_wins}s} │ {'Wins as B':^{spacing_wins}s} │ {'Draws':^{spacing_wins}s} │ {'Draws as A':^{spacing_wins}s} │ {'Draws as B':^{spacing_wins}s} │ {'Avg Moves':^{spacing_moves}s} │\n")
        # Sort by number of wins
        for winner, overall_result in sorted(overall_results.items(), key=lambda pairing: pairing[1].wins,
                                             reverse=True):
            # write spacer
            overall_file.write(
                "├─" + ("─" * spacing_teams + "─┼─") + ("─" * spacing_wins + "─┼─") * 6 + "─" * spacing_moves + "─┤\n")
            # write result
            avg_moves = f"{overall_result.avg_moves / ((len(overall_results.keys()) - 1) * 2):.2f}"
            overall_file.write(
                f"│ {winner:^{spacing_teams}} │ {overall_result.wins:^{spacing_wins}} │ {overall_result.wins_A:^{spacing_wins}} │ {overall_result.wins_B:^{spacing_wins}} │ {overall_result.draws:^{spacing_wins}} │ {overall_result.draws_A:^{spacing_wins}} │ {overall_result.draws_B:^{spacing_wins}} │ {avg_moves:^{spacing_moves}} │\n")
        overall_file.write(
            "└─" + "─" * spacing_teams + "─┴─" + ("─" * spacing_wins + "─┴─") * 6 + "─" * spacing_moves + "─┘\n")


def save_games(results: List[GameResult]):
    """
    Function to store individual games in file

    :param results: List of all game results
    """
    # Default spacings
    spacing_teams = 8
    spacing_moves = 5
    with open("games.txt", 'w') as game_file:
        game_file.write(
            "┌─" + "─" * spacing_teams + "─┬─" + "─" * spacing_teams + "─┬─" + "─" * spacing_teams + "─┬─" + "─" * spacing_moves + "─┐\n")
        game_file.write(
            f"│ {'Player A':^{spacing_teams}s} │ {'Player B':^{spacing_teams}s} │ {'Winner':^{spacing_teams}s} │ {'Moves':^{spacing_moves}s} |\n")
        # Sort by team names
        for result in sorted(results, key=lambda entry: (entry.player_A, entry.player_B)):
            game_file.write(
                "├─" + "─" * spacing_teams + "─┼─" + "─" * spacing_teams + "─┼─" + "─" * spacing_teams + "─┼─" + "─" * spacing_moves + "─┤\n")
            game_file.write(
                f"│ {result.player_A:^{spacing_teams}} │ {result.player_B:^{spacing_teams}} │ {result.winner if not result.is_draw else 'O':^{spacing_teams}} │ {result.number_of_moves:^{spacing_moves}} │\n")
        game_file.write(
            "└─" + "─" * spacing_teams + "─┴─" + "─" * spacing_teams + "─┴─" + "─" * spacing_teams + "─┴─" + "─" * spacing_moves + "─┘\n")


def main():
    groups = get_groups()
    results = simulate_games(groups, silent=True)
    save_overall(results)
    save_games(results)


if __name__ == "__main__":
    main()
