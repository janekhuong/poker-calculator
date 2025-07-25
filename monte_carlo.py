import random
from typing import List, Optional, Dict
from cards import Deck, Card
from game_simulator import Player, simulate_hand


def simulate_win_odds(
    players: List[Player],
    board_cards: Optional[List[Card]] = None,
    trials: int = 10000,
    verbose: bool = True,
) -> Dict[str, Dict[str, float]]:
    win_counts = {p.name: 0 for p in players}
    tie_counts = {p.name: 0 for p in players}

    for _ in range(trials):
        # Copy the players and board so we don't mutate input state
        sim_players = [Player(p.name, p.hole_cards.copy()) for p in players]
        sim_board = board_cards.copy() if board_cards else None

        try:
            _, sim_players, winners = simulate_hand(
                sim_players, sim_board, verbose=False
            )
        except Exception as e:
            # Safety catch in case of invalid state
            continue

        if len(winners) == 1:
            win_counts[winners[0].name] += 1
        else:
            for p in winners:
                tie_counts[p.name] += 1

    results = {}
    for p in players:
        wins = win_counts[p.name]
        ties = tie_counts[p.name]
        total = trials
        results[p.name] = {
            "win_pct": round(100 * wins / total, 2),
            "tie_pct": round(100 * ties / total, 2),
            "loss_pct": round(100 * (1 - (wins + ties) / total), 2),
        }

    if verbose:
        print("\n--- Monte Carlo Simulation Results ---")
        for name, stats in results.items():
            print(
                f"{name}: Win {stats['win_pct']}%, Tie {stats['tie_pct']}%, Loss {stats['loss_pct']}%"
            )

    return results

