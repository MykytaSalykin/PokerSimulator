import pytest
from src.deck import Deck

def test_deck_initialization():
    deck = Deck()
    assert len(deck.cards) == 52
    assert "AH" in deck.cards
    assert "2S" in deck.cards

def test_deal():
    deck = Deck()
    hand = deck.deal(5)
    assert len(hand) == 5
    assert len(deck.cards) == 47

def test_full_name_suit():
    assert Deck.full_name_suit("H") == "Hearts"
    assert Deck.full_name_suit("X") == "Unknown"