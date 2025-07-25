import random
from typing import List, Optional, Dict
from cards import Deck, Card
from game_simulator import Player, simulate_hand, compare_hands


def simulate_win_odds(
    players: List[Player],
    board_cards: Optional[List[Card]] = None,
    trials: int = 10000,
    verbose: bool = True,
) -> Dict[str, Dict[str, float]]:
    """
    Simulate many poker hands and return win/tie probabilities for each player.
    Automatically removes card conflicts and uses tie-breakers for equal-ranked hands.
    """
    win_counts = {p.name: 0 for p in players}
    tie_counts = {p.name: 0 for p in players}

    for _ in range(trials):
        # Step 1: Track all known cards
        known_cards = []
        for p in players:
            known_cards.extend(p.hole_cards)
        if board_cards:
            known_cards.extend(board_cards)

        # Step 2: Build deck and remove known cards
        deck = Deck()
        deck.remove_multiple(known_cards)

        # Step 3: Copy players and fill in missing hole cards
        sim_players = []
        for p in players:
            copied = Player(p.name, p.hole_cards.copy())
            while len(copied.hole_cards) < 2:
                drawn = deck.draw(1)[0]
                copied.hole_cards.append(drawn)
            sim_players.append(copied)

        # Step 4: Complete the board (up to 5 cards)
        sim_board = board_cards.copy() if board_cards else []
        while len(sim_board) < 5:
            sim_board.append(deck.draw(1)[0])

        # Step 5: Simulate a full hand
        try:
            _, sim_players, winners = simulate_hand(
                sim_players, sim_board, verbose=False
            )
        except Exception:
            continue

        # Step 6: Count outcomes
        if len(winners) == 1:
            win_counts[winners[0].name] += 1
        else:
            for p in winners:
                tie_counts[p.name] += 1

    # Step 7: Compute final percentages
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

    # Optional display
    if verbose:
        print("\n--- Monte Carlo Simulation Results ---")
        for name, stats in results.items():
            print(
                f"{name}: Win {stats['win_pct']}%, Tie {stats['tie_pct']}%, Loss {stats['loss_pct']}%"
            )

    return results
