import random 
from typing import List 

# constants
SUITS = ['S', 'H', 'D', 'C'] # spades, hearts, diamonds, clubs 
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
RANK_TO_VALUE = {r: i for i, r in enumerate(RANKS)}


class Card:
    def __init__(self, rank: str, suit: str):
        self.rank = rank
        self.suit = suit
        self.value = RANK_TO_VALUE[rank]

    def __str__(self):
        return f"{self.rank}{self.suit}"

    def __repr__(self):
        return f"Card('{self.rank}', '{self.suit}')"

    def __eq__(self, other):
        return self.rank == other.rank and self.suit == other.suit

    def __hash__(self):
        return hash((self.rank, self.suit))


class Deck:
    def __init__(self):
        self.cards = [Card(rank, suit) for suit in SUITS for rank in RANKS]
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self, n: int) -> List[Card]:
        return [self.cards.pop() for _ in range(n)]

    def remove(self, card: Card):
        self.cards = [c for c in self.cards if c != card]

    def remove_multiple(self, cards: List[Card]):
        for card in cards:
            self.remove(card)

    def __len__(self):
        return len(self.cards)

    def __repr__(self):
        return f"Deck({len(self.cards)} cards remaining)"


def parse_card(card_str: str) -> Card:
    # Parses a string like 'AS' or 'TD' into a Card
    if len(card_str) != 2:
        raise ValueError(f"Invalid card string: {card_str}")
    rank = card_str[0].upper()
    suit = card_str[1].upper()
    return Card(rank, suit)


def parse_cards(card_strs: List[str]) -> List[Card]:
    # Parses list of strings like ['AS', 'TD'] into Card objects
    return [parse_card(cs) for cs in card_strs]
