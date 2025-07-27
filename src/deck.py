import random

class Deck:
    def __init__(self):
        self.suits = ["H", "D", "C", "S"]
        self.ranks = [str(i) for i in range(2, 11)] + ["J", "Q", "K", "A"]
        self.reset()

    def reset(self):
        self.cards = [rank + suit for suit in self.suits for rank in self.ranks]
        random.seed()

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self, num_cards):
        if len(self.cards) < num_cards:
            raise ValueError("Not enough cards in deck")
        dealt_cards = self.cards[:num_cards]
        self.cards = self.cards[num_cards:]
        return dealt_cards