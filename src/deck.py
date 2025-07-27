import random

class Deck:
    def __init__(self):
        self.suits = ["H", "D", "C", "S"]
        self.ranks = [str(i) for i in range(2, 11)] + ["J", "Q", "K", "A"]
        self.cards = [rank + suit for suit in self.suits for rank in self.ranks]

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self, n=5):
        if len(self.cards) < n:
            raise ValueError("Not enough cards in deck")
        hand = self.cards[:n]
        self.cards = self.cards[n:]
        return hand

    def reset(self):
        self.cards = [rank + suit for suit in self.suits for rank in self.ranks]

    @staticmethod
    def full_name_suit(suit):
        suit_map = {"H": "Hearts", "D": "Diamonds", "C": "Clubs", "S": "Spades"}
        return suit_map.get(suit, "Unknown")