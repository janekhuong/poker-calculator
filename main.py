import random
from cards import parse_cards
from game_simulator import Player
from monte_carlo import simulate_win_odds

players = [
    Player("Hero", parse_cards(["AS", "AD"])),  # Pocket Aces
    Player("Villain", parse_cards(["5H", "2D"])),  # Specific hand
]

board = parse_cards(["JC", "6H", "3H"])  # partial board

simulate_win_odds(players, board, trials=10000)
