from src.deck import Deck
from src.hand_evaluator import HandEvaluator

class PokerGame:
    def __init__(self):
        self.deck = Deck()
        self.evaluator = HandEvaluator()
        self.probabilities = {
            "Royal Flush": 0.000154,
            "Straight Flush": 0.00139,
            "Four of a Kind": 0.0240,
            "Full House": 0.140,
            "Flush": 0.196,
            "Straight": 0.39,
            "Three of a Kind": 2.11,
            "Two Pair": 4.75,
            "One Pair": 42.2,
            "High Card": 50.1
        }

    def deal_hands(self, num_hands=1):
        self.deck.reset()
        self.deck.shuffle()
        return [self.deck.deal(5) for _ in range(num_hands)]

    def play(self, hand1, hand2, bet=0):
        result = self.evaluator.compare_hands(hand1, hand2)
        result["bet"] = bet
        return result

    def get_probability(self, hand):
        rank, _ = self.evaluator.evaluate(hand)
        return self.probabilities.get(rank, 0.0)