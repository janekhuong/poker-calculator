import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from cards import parse_cards
from hand_evaluator import evaluate_hand


def test_royal_flush():
    cards = parse_cards(["AS", "KS", "QS", "JS", "TS", "2D", "3C"])
    rank, _, name = evaluate_hand(cards)
    assert rank == 8
    assert name == "Straight Flush"


def test_four_of_a_kind():
    cards = parse_cards(["9C", "9D", "9H", "9S", "2C", "3D", "4H"])
    rank, _, name = evaluate_hand(cards)
    assert rank == 7
    assert name == "Four of a Kind"


def test_full_house():
    cards = parse_cards(["KH", "KS", "KD", "2H", "2D", "9C", "3S"])
    rank, _, name = evaluate_hand(cards)
    assert rank == 6
    assert name == "Full House"


def test_flush():
    cards = parse_cards(["2H", "6H", "9H", "KH", "TH", "3D", "4C"])
    rank, _, name = evaluate_hand(cards)
    assert rank == 5
    assert name == "Flush"


def test_straight():
    cards = parse_cards(["4C", "5D", "6H", "7S", "8C", "2H", "9D"])
    rank, _, name = evaluate_hand(cards)
    assert rank == 4
    assert name == "Straight"


def test_ace_low_straight():
    cards = parse_cards(["AS", "2C", "3D", "4H", "5S", "8H", "KD"])
    rank, _, name = evaluate_hand(cards)
    assert rank == 4
    assert name == "Straight"


def test_three_of_a_kind():
    cards = parse_cards(["5C", "5D", "5S", "2H", "9C", "KH", "QS"])
    rank, _, name = evaluate_hand(cards)
    assert rank == 3
    assert name == "Three of a Kind"


def test_two_pair():
    cards = parse_cards(["JC", "JD", "8H", "8S", "3C", "KH", "2D"])
    rank, _, name = evaluate_hand(cards)
    assert rank == 2
    assert name == "Two Pair"


def test_one_pair():
    cards = parse_cards(["QC", "QD", "6H", "7S", "3C", "8D", "2S"])
    rank, _, name = evaluate_hand(cards)
    assert rank == 1
    assert name == "One Pair"


def test_high_card():
    cards = parse_cards(["AS", "KD", "9H", "6S", "3C", "2D", "8H"])
    rank, _, name = evaluate_hand(cards)
    assert rank == 0
    assert name == "High Card"
