from collections import Counter

class HandEvaluator:
    def __init__(self):
        self.rank_values = {str(i): i for i in range(2, 11)}
        self.rank_values.update({"J": 11, "Q": 12, "K": 13, "A": 14})
        self.hand_ranks = {
            "Royal Flush": 10,
            "Straight Flush": 9,
            "Four of a Kind": 8,
            "Full House": 7,
            "Flush": 6,
            "Straight": 5,
            "Three of a Kind": 4,
            "Two Pair": 3,
            "One Pair": 2,
            "High Card": 1
        }

    def evaluate(self, hand):
        ranks = [card[:-1] for card in hand]
        suits = [card[-1] for card in hand]
        rank_counts = Counter(ranks)
        values = sorted([self.rank_values[rank] for rank in ranks])
        is_flush = len(set(suits)) == 1
        is_straight = len(set(values)) == 5 and max(values) - min(values) == 4

        if is_flush and is_straight and min(values) == 10:
            return "Royal Flush", values
        if is_flush and is_straight:
            return "Straight Flush", values
        if 4 in rank_counts.values():
            return "Four of a Kind", values
        if sorted(rank_counts.values()) == [2, 3]:
            return "Full House", values
        if is_flush:
            return "Flush", values
        if is_straight:
            return "Straight", values
        if 3 in rank_counts.values():
            return "Three of a Kind", values
        if sorted(rank_counts.values()) == [1, 2, 2]:
            return "Two Pair", values
        if 2 in rank_counts.values():
            return "One Pair", values
        return "High Card", values

    def compare_hands(self, hand1, hand2):
        rank1, values1 = self.evaluate(hand1)
        rank2, values2 = self.evaluate(hand2)
        if self.hand_ranks[rank1] > self.hand_ranks[rank2]:
            return {"winner": "Hand 1", "hand": hand1, "rank": rank1}
        elif self.hand_ranks[rank1] < self.hand_ranks[rank2]:
            return {"winner": "Hand 2", "hand": hand2, "rank": rank2}
        else:
            for v1, v2 in zip(reversed(values1), reversed(values2)):
                if v1 > v2:
                    return {"winner": "Hand 1", "hand": hand1, "rank": rank1}
                elif v1 < v2:
                    return {"winner": "Hand 2", "hand": hand2, "rank": rank2}
            return {"winner": "Tie", "hand": hand1, "rank": rank1}