from typing import List, Optional
from cards import Deck, Card
from hand_evaluator import evaluate_hand


class Player:
    def __init__(self, name: str, hole_cards: Optional[List[Card]] = None):
        self.name = name
        self.hole_cards = hole_cards or []
        self.best_hand = []
        self.hand_rank = -1
        self.hand_name = ""
        self.win = False

    def __repr__(self):
        cards = " ".join(str(card) for card in self.hole_cards)
        return f"{self.name} ({cards})"


def simulate_hand(
    players: List[Player],
    board_cards: Optional[List[Card]] = None,
    verbose: bool = True,
):
    deck = Deck()

    # Remove known cards from the deck
    known_cards = []
    for p in players:
        known_cards.extend(p.hole_cards)
    if board_cards:
        known_cards.extend(board_cards)

    deck.remove_multiple(known_cards)

    # Fill in any missing hole cards
    for p in players:
        while len(p.hole_cards) < 2:
            p.hole_cards.append(deck.draw(1)[0])

    # Deal remaining community cards (up to 5 total)
    board = board_cards or []
    while len(board) < 5:
        board.append(deck.draw(1)[0])

    # Evaluate each player
    for p in players:
        full_hand = p.hole_cards + board
        rank, best_hand, hand_name = evaluate_hand(full_hand)
        p.hand_rank = rank
        p.best_hand = best_hand
        p.hand_name = hand_name

    # Find winner(s)
    max_rank = max(p.hand_rank for p in players)
    candidates = [p for p in players if p.hand_rank == max_rank]

    # Break ties using best hand comparison
    winners = []
    for p in candidates:
        if not winners:
            winners.append(p)
        else:
            cmp = compare_hands(p.best_hand, winners[0].best_hand)
            if cmp > 0:
                winners = [p]  # new winner
            elif cmp == 0:
                winners.append(p)  # tie

    if verbose:
        print("\n--- Board ---")
        print(" ".join(str(c) for c in board))
        print("\n--- Players ---")
        for p in players:
            print(f"{p.name}: {p.hole_cards[0]} {p.hole_cards[1]} → {p.hand_name}")
        print("\nWinner(s):", ", ".join(p.name for p in winners))

    return board, players, winners


def compare_hands(hand1: List[Card], hand2: List[Card]) -> int:
    values1 = sorted([c.value for c in hand1], reverse=True)
    values2 = sorted([c.value for c in hand2], reverse=True)
    for v1, v2 in zip(values1, values2):
        if v1 > v2:
            return 1
        elif v1 < v2:
            return -1
    return 0
