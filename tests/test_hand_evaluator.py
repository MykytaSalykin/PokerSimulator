import pytest
from src.hand_evaluator import HandEvaluator

@pytest.fixture
def evaluator():
    return HandEvaluator()

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