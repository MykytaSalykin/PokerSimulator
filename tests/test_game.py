import pytest
from src.game import PokerGame
from src.deck import Deck
from src.hand_evaluator import HandEvaluator

@pytest.fixture
def game():
    return PokerGame()

def test_deal_hands(game):
    (player_hole, opponent_hole), community_cards = game.deal_hands(2)
    assert len(player_hole) == 2
    assert len(opponent_hole) == 2
    assert len(community_cards) == 5
    deck = Deck()
    deck_cards = set(deck.cards)
    dealt_cards = set(player_hole + opponent_hole + community_cards)
    assert dealt_cards.issubset(deck_cards)
    assert len(dealt_cards) == 9  # 2 + 2 + 5 unique cards

def test_opponent_action(game):
    action, bet = game.opponent_action(2, 3, "preflop", ["AH", "KH"], [], 100, 0, 100)
    assert action in ["call", "raise", "fold"]
    if action == "raise":
        assert bet >= 2
    elif action == "call":
        assert bet == 2
    elif action == "fold":
        assert bet == 0

def test_play_result(game):
    player_hole = ["AH", "KH"]
    opponent_hole = ["2C", "3D"]
    community_cards = ["10H", "JH", "QH", "2C", "3D"]
    result = game.play(player_hole, opponent_hole, community_cards, 20, 10)
    assert result["winner"] == "Player"
    assert result["rank"] == "Royal Flush"
    assert result["pot"] == 20