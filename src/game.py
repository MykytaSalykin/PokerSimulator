import random
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
            "Full House": 0.1441,
            "Flush": 0.1967,
            "Straight": 0.3925,
            "Three of a Kind": 2.1128,
            "Two Pair": 4.7539,
            "One Pair": 42.2569,
            "High Card": 50.1177,
        }

    def deal_hands(self, num_players=2):
        self.deck.reset()
        self.deck.shuffle()
        hole_cards = [self.deck.deal(2) for _ in range(num_players)]
        community_cards = self.deck.deal(5)
        return hole_cards, community_cards

    def evaluate_best_hand(self, hole_cards, community_cards):
        all_cards = hole_cards + community_cards
        if len(all_cards) < 5:
            return "High Card", [
                self.evaluator.rank_values[card[:-1]] for card in hole_cards
            ]
        best_rank, best_values = (
            "High Card",
            [self.evaluator.rank_values[card[:-1]] for card in all_cards],
        )
        for i in range(len(all_cards)):
            for j in range(i + 1, len(all_cards)):
                subset = all_cards[:i] + all_cards[i + 1 : j] + all_cards[j + 1 :]
                rank, values = self.evaluator.evaluate(subset)
                if (
                    self.evaluator.hand_ranks[rank]
                    > self.evaluator.hand_ranks[best_rank]
                ):
                    best_rank, best_values = rank, values
                elif (
                    self.evaluator.hand_ranks[rank]
                    == self.evaluator.hand_ranks[best_rank]
                ):
                    if values and (not best_values or max(values) > max(best_values)):
                        best_rank, best_values = rank, values
        return best_rank, best_values

    def evaluate_pocket_strength(self, hole_cards):
        ranks = [card[:-1] for card in hole_cards]
        suits = [card[-1] for card in hole_cards]
        values = sorted([self.evaluator.rank_values[rank] for rank in ranks])
        is_pair = values[0] == values[1]
        is_suited = suits[0] == suits[1]
        gap = values[1] - values[0]
        strength = 0
        if is_pair:
            strength += values[0] * 0.5
        elif is_suited:
            strength += 2
        if gap <= 3:
            strength += (4 - gap) * 0.5
        strength += max(values) * 0.3
        return min(strength, 10)

    def opponent_action(
        self,
        current_bet,
        pot,
        street,
        opponent_hole,
        community_cards,
        opponent_money,
        raise_count,
        player_money,
    ):
        strength = (
            self.evaluate_pocket_strength(opponent_hole)
            if street == "preflop"
            else self.evaluator.hand_ranks[
                self.evaluate_best_hand(opponent_hole, community_cards)[0]
            ]
        )
        if random.random() < 0.1 and strength < 3:
            return "fold", 0
        if current_bet > 0:
            pot_odds = current_bet / (pot + current_bet)
            if (
                strength >= 6 or (random.random() < 0.3 and strength >= 3)
            ) and raise_count < 4:
                raise_amount = max(
                    current_bet * 2, min(int(pot * 0.5), opponent_money, player_money)
                )
                return "raise", raise_amount
            if strength >= 3 or random.random() < 0.5:
                return "call", current_bet
            return "fold", 0
        if strength >= 5 or (random.random() < 0.3 and strength >= 3):
            bet_amount = max(1, min(int(pot * 0.2), opponent_money, player_money))
            return "bet", bet_amount
        return "check", 0

    def play(self, player_hole, opponent_hole, community_cards, pot, player_total_bet):
        player_rank, player_values = self.evaluate_best_hand(
            player_hole, community_cards
        )
        opponent_rank, opponent_values = self.evaluate_best_hand(
            opponent_hole, community_cards
        )
        if (
            self.evaluator.hand_ranks[player_rank]
            > self.evaluator.hand_ranks[opponent_rank]
        ):
            return {
                "winner": "Player",
                "hand": player_hole,
                "rank": player_rank,
                "pot": pot,
            }
        elif (
            self.evaluator.hand_ranks[player_rank]
            < self.evaluator.hand_ranks[opponent_rank]
        ):
            return {
                "winner": "Opponent",
                "hand": opponent_hole,
                "rank": opponent_rank,
                "pot": -player_total_bet,
            }
        else:
            # Compare up to 5 kickers
            player_all_cards = sorted(
                [
                    self.evaluator.rank_values[card[:-1]]
                    for card in player_hole + community_cards
                ],
                reverse=True,
            )[:5]
            opponent_all_cards = sorted(
                [
                    self.evaluator.rank_values[card[:-1]]
                    for card in opponent_hole + community_cards
                ],
                reverse=True,
            )[:5]
            for v1, v2 in zip(player_all_cards, opponent_all_cards):
                if v1 > v2:
                    return {
                        "winner": "Player",
                        "hand": player_hole,
                        "rank": player_rank,
                        "pot": pot,
                    }
                elif v1 < v2:
                    return {
                        "winner": "Opponent",
                        "hand": opponent_hole,
                        "rank": opponent_rank,
                        "pot": -player_total_bet,
                    }
            return {"winner": "Tie", "hand": player_hole, "rank": player_rank, "pot": 0}

    def get_probability(self, hand):
        rank, _ = self.evaluator.evaluate(hand)
        return self.probabilities.get(rank, 0.0)
