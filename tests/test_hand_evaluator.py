import pytest
from src.hand_evaluator import HandEvaluator
from src.game import PokerGame

@pytest.fixture
def evaluator():
    return HandEvaluator()

@pytest.fixture
def game():
    return PokerGame()

def test_royal_flush(evaluator):
    hand = ["10H", "JH", "QH", "KH", "AH"]
    rank, _ = evaluator.evaluate(hand)
    assert rank == "Royal Flush"

def test_straight_flush(evaluator):
    hand = ["9H", "10H", "JH", "QH", "KH"]
    rank, _ = evaluator.evaluate(hand)
    assert rank == "Straight Flush"

def test_compare_hands(evaluator):
    hand1 = ["10H", "JH", "QH", "KH", "AH"]
    hand2 = ["9H", "10H", "JH", "QH", "KH"]
    result = evaluator.compare_hands(hand1, hand2)
    assert result["winner"] == "Hand 1"

def test_holdem_evaluation(game):
    player_hole = ["AH", "KH"]
    community = ["10H", "JH", "QH", "2C", "3D"]
    rank, _ = game.evaluate_best_hand(player_hole, community)
    assert rank == "Royal Flush"

def test_opponent_action(game):
    action, amount = game.opponent_action(2, 3, "preflop", ["AH", "KH"], [], 100, 0, 100)
    assert action in ["fold", "call", "raise"]
    if action != "fold":
        assert amount >= 0

def test_empty_values(game):
    player_hole = ["AH", "KH"]
    community = []
    rank, values = game.evaluate_best_hand(player_hole, community)
    assert rank == "High Card"
    assert values == [14, 13]

def test_raise_limit(game):
    action, amount = game.opponent_action(10, 20, "preflop", ["AH", "KH"], [], 100, 4, 100)
    assert action != "raise"