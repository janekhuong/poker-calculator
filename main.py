import random
from cards import parse_cards
from game_simulator import Player
from monte_carlo import simulate_win_odds

random.seed(42)

players = [Player("Hero", parse_cards(["AS", "AD"])), Player("Villain")]  # random cards
board = parse_cards(["2C", "7D", "9H"])  # partial board

simulate_win_odds(players, board, trials=5000)
