import random

class Deck:
    def __init__(self):
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        suits = ['H', 'D', 'C', 'S']
        self.cards = [rank + suit for rank in ranks for suit in suits]
    
    def shuffle(self):
        random.shuffle(self.cards)
    
    def deal(self, num_cards):
        if num_cards > len(self.cards):
            return []
        dealt_cards = self.cards[:num_cards]
        self.cards = self.cards[num_cards:]
        return dealt_cards
    
    def reset(self):
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        suits = ['H', 'D', 'C', 'S']
        self.cards = [rank + suit for rank in ranks for suit in suits]
    
    @staticmethod
    def full_name_suit(suit):
        suit_map = {'H': 'Hearts', 'D': 'Diamonds', 'C': 'Clubs', 'S': 'Spades'}
        return suit_map.get(suit, 'Unknown')