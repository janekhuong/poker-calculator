from collections import Counter
from itertools import combinations
from typing import List, Tuple
from cards import Card, RANKS, RANK_TO_VALUE

HAND_RANKS = [
    "High Card",  # 0
    "One Pair",  # 1
    "Two Pair",  # 2
    "Three of a Kind",  # 3
    "Straight",  # 4
    "Flush",  # 5
    "Full House",  # 6
    "Four of a Kind",  # 7
    "Straight Flush",  # 8
    "Royal Flush",  # 9
]


def evaluate_hand(cards: List[Card]) -> Tuple[int, List[Card], str]:
    best_rank = -1
    best_hand = []
    best_name = ""

    for combo in combinations(cards, 5):
        rank, name = rank_five_card_hand(list(combo))
        if rank > best_rank:
            best_rank = rank
            best_hand = combo
            best_name = name

    return best_rank, list(best_hand), best_name


def rank_five_card_hand(cards: List[Card]) -> Tuple[int, str]:
    ranks = sorted([c.value for c in cards], reverse=True)
    suits = [c.suit for c in cards]
    rank_counts = Counter(ranks)
    is_flush = len(set(suits)) == 1
    is_straight, high_card = check_straight(ranks)

    if is_flush and is_straight:
        if set(ranks) == set([12, 11, 10, 9, 8]):
            return 9, "Royal Flush"
        else:
            return 8, "Straight Flush"
    if 4 in rank_counts.values():
        return 7, "Four of a Kind"
    if 3 in rank_counts.values() and 2 in rank_counts.values():
        return 6, "Full House"
    if is_flush:
        return 5, "Flush"
    if is_straight:
        return 4, "Straight"
    if 3 in rank_counts.values():
        return 3, "Three of a Kind"
    if list(rank_counts.values()).count(2) == 2:
        return 2, "Two Pair"
    if 2 in rank_counts.values():
        return 1, "One Pair"
    return 0, "High Card"


def check_straight(values: List[int]) -> Tuple[bool, int]:
    # Check for a straight (5 consecutive values)
    unique = sorted(set(values), reverse=True)

    # Handle ace-low straight (A,2,3,4,5)
    if set([12, 0, 1, 2, 3]).issubset(set(values)):
        return True, 3  # 5-high straight

    for i in range(len(unique) - 4):
        if unique[i] - unique[i + 4] == 4:
            return True, unique[i]
    return False, -1
