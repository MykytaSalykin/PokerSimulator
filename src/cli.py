import click
import json
from src.deck import Deck
from src.game import PokerGame

@click.group()
def cli():
    pass

@cli.command("info")
@click.option("--probability", is_flag=True, help="Display probabilities of poker hands")
def info(probability):
    game = PokerGame()
    for rank, value in game.evaluator.hand_ranks.items():
        if probability:
            prob = game.probabilities[rank]
            click.secho(f"{rank}: {value} - {prob:.4f}% - 1 in {1/prob:,.0f}", fg="yellow")
        else:
            click.secho(f"{rank}: {value}", fg="green")

@cli.command("deal")
@click.option("--hands", default=1, help="Number of hands to deal")
def deal(hands):
    game = PokerGame()
    hands_dealt, community_cards = game.deal_hands(hands)
    flop = ", ".join(community_cards[:3])
    for hand in hands_dealt:
        cards = ", ".join(hand)
        color = "red" if hand[0][-1] in ["H", "D"] else "black"
        click.secho(f"Your cards: {cards}", fg=color)
        click.secho(f"Flop: {flop}", fg="green")
        rank, _ = game.evaluator.evaluate(hand + community_cards[:3])
        click.secho(f"Hand Rank (with flop): {rank}", fg="green")
    click.echo()

@cli.command("play")
@click.option("--name", default="Player", help="Player name")
@click.option("--bet", default=1, help="Amount to bet", type=click.IntRange(1, 1000))
def play(name, bet):
    game = PokerGame()
    (player_hole, opponent_hole), community_cards = game.deal_hands(2)
    pot = bet * 2
    cards = ", ".join(player_hole)
    color = "red" if player_hole[0][-1] in ["H", "D"] else "black"
    click.secho(f"Your cards: {cards}", fg=color)
    click.secho(f"Flop: {', '.join(community_cards[:3])}", fg="green")
    click.secho(f"Turn: {community_cards[3]}", fg="green")
    click.secho(f"With Turn: {', '.join(community_cards[:4])}", fg="green")
    click.secho(f"River: {community_cards[4]}", fg="green")
    click.secho(f"With River: {', '.join(community_cards)}", fg="green")
    result = game.play(player_hole, opponent_hole, community_cards, pot, bet)
    click.secho(f"Your hand: {player_hole} + {community_cards} -> {result['rank']}", fg="blue")
    click.secho(f"Opponent's hand: {opponent_hole} + {community_cards} -> {result['rank'] if result['winner'] == 'Tie' else game.evaluate_best_hand(opponent_hole, community_cards)[0]}", fg="blue")
    if result["winner"] == "Player":
        click.secho(f"{name} wins ${pot} with {result['rank']}!", fg="green")
    elif result["winner"] == "Opponent":
        click.secho(f"{name} loses ${-result['pot']} against Opponent's {result['rank']}!", fg="red")
    else:
        click.secho("It's a tie!", fg="yellow")

@cli.command("interactive")
@click.option("--name", default="Player", help="Player name")
@click.option("--rounds", default=1, help="Number of rounds")
@click.option("--money", default=100, help="Starting money", type=click.IntRange(10, 1000))
def interactive(name, rounds, money):
    game = PokerGame()
    history = {
        "rounds": 0, "wins": 0, "losses": 0, "ties": 0,
        "money": money, "bets": {}, "probabilities": {}, "hands": {}
    }
    small_blind, big_blind = 1, 2
    for i in range(1, rounds + 1):
        player_total_bet = 0  # Track total bets for this round
        click.secho(f"Round {i}: Money: ${history['money']}", fg="blue")
        if history['money'] < big_blind:
            click.secho("Not enough money for big blind! Game over.", fg="red")
            break
        (player_hole, opponent_hole), community_cards = game.deal_hands(2)
        pot = small_blind + big_blind
        history["money"] -= big_blind
        player_total_bet += big_blind
        opponent_money = history["money"]
        click.secho(f"Blinds: Small Blind ${small_blind}, Big Blind ${big_blind} (deducted)", fg="yellow")
        cards = ", ".join(player_hole)
        color = "red" if player_hole[0][-1] in ["H", "D"] else "black"
        click.secho(f"Your cards: {cards}", fg=color)
        # Pre-flop betting
        current_bet = big_blind
        raise_count = 0
        while True:
            if history["money"] == 0:
                click.secho(f"{name} is all-in!", fg="yellow")
                opponent_action, opponent_bet = game.opponent_action(current_bet, pot, "preflop", opponent_hole, [], opponent_money, raise_count, history["money"])
                click.secho(f"Opponent: {opponent_action.capitalize()} ${opponent_bet}", fg="yellow")
                if opponent_action == "call":
                    pot += opponent_bet
                    opponent_money -= opponent_bet
                elif opponent_action == "fold":
                    history["wins"] += 1
                    history["money"] += pot
                    click.secho(f"Opponent folds! {name} wins ${pot}.", fg="green")
                    break
                break
            click.secho(f"Money: ${history['money']}", fg="blue")
            click.secho(f"Your cards: {cards}", fg=color)
            action = click.prompt(f"Pre-flop (Pot ${pot}): Call ${current_bet}, Raise <amount>, Fold, or Finish", type=str)
            action = action.lower().replace('$', '').strip()
            if action == "finish":
                click.secho("Game ended by player.", fg="yellow")
                break
            elif action == "fold":
                history["losses"] += 1
                click.secho(f"{name} folds! Opponent wins ${pot}.", fg="red")
                break
            elif action == "call":
                if current_bet <= history['money']:
                    history["money"] -= current_bet
                    player_total_bet += current_bet
                    pot += current_bet
                    opponent_action, opponent_bet = game.opponent_action(current_bet, pot, "preflop", opponent_hole, [], opponent_money, raise_count, history["money"])
                    click.secho(f"Opponent: {opponent_action.capitalize()} ${opponent_bet}", fg="yellow")
                    if opponent_action == "fold":
                        history["wins"] += 1
                        history["money"] += pot
                        click.secho(f"Opponent folds! {name} wins ${pot}.", fg="green")
                        break
                    elif opponent_action == "call":
                        pot += opponent_bet
                        opponent_money -= opponent_bet
                        break
                    elif opponent_action == "raise" and raise_count < 4:
                        current_bet = opponent_bet
                        pot += opponent_bet
                        opponent_money -= opponent_bet
                        raise_count += 1
                        if raise_count >= 4:  # Max 4 raises per street
                            break
                    else:
                        break
                else:
                    click.secho(f"Not enough money! Max bet ${history['money']}.", fg="red")
            elif action.startswith("raise "):
                try:
                    amount = int(action.split()[1])
                    if amount >= current_bet and amount <= history['money'] and raise_count < 4:
                        history["money"] -= amount
                        player_total_bet += amount
                        pot += amount
                        current_bet = amount
                        raise_count += 1
                        opponent_action, opponent_bet = game.opponent_action(current_bet, pot, "preflop", opponent_hole, [], opponent_money, raise_count, history["money"])
                        click.secho(f"Opponent: {opponent_action.capitalize()} ${opponent_bet}", fg="yellow")
                        if opponent_action == "fold":
                            history["wins"] += 1
                            history["money"] += pot
                            click.secho(f"Opponent folds! {name} wins ${pot}.", fg="green")
                            break
                        elif opponent_action == "call":
                            pot += opponent_bet
                            opponent_money -= opponent_bet
                            break
                        elif opponent_action == "raise" and raise_count < 4:
                            current_bet = opponent_bet
                            pot += opponent_bet
                            opponent_money -= opponent_bet
                            raise_count += 1
                            if raise_count >= 4:  # Max 4 raises per street
                                break
                        else:
                            break
                    else:
                        click.secho(f"Invalid raise! Must be between ${current_bet} and ${history['money']}.", fg="red")
                except:
                    click.secho("Invalid raise format! Use 'raise <amount>'.", fg="red")
            else:
                click.secho("Invalid action! Use 'call', 'raise <amount>', 'fold', or 'finish'.", fg="red")
        if action == "fold" or opponent_action == "fold" or action == "finish":
            if action == "finish":
                break
            continue
        # Flop
        click.secho(f"Flop: {', '.join(community_cards[:3])}", fg="green")
        click.secho(f"With Flop: {', '.join(community_cards[:3])}", fg="green")
        current_bet = 0
        raise_count = 0
        while True:
            if history["money"] == 0:
                click.secho(f"{name} is all-in!", fg="yellow")
                break
            click.secho(f"Money: ${history['money']}", fg="blue")
            click.secho(f"Your cards: {cards}", fg=color)
            action_prompt = f"Flop (Pot ${pot}): Check, Bet <amount>, Fold, or Finish" if current_bet == 0 else f"Flop (Pot ${pot}): Call ${current_bet}, Raise <amount>, Fold, or Finish"
            action = click.prompt(action_prompt, type=str)
            action = action.lower().replace('$', '').strip()
            if action == "finish":
                click.secho("Game ended by player.", fg="yellow")
                break
            elif action == "fold":
                history["losses"] += 1
                click.secho(f"{name} folds! Opponent wins ${pot}.", fg="red")
                break
            elif action == "check" and current_bet == 0:
                opponent_action, opponent_bet = game.opponent_action(current_bet, pot, "flop", opponent_hole, community_cards[:3], opponent_money, raise_count, history["money"])
                click.secho(f"Opponent: {opponent_action.capitalize()} ${opponent_bet}", fg="yellow")
                if opponent_action == "fold":
                    history["wins"] += 1
                    history["money"] += pot
                    click.secho(f"Opponent folds! {name} wins ${pot}.", fg="green")
                    break
                elif opponent_action == "check":
                    break
                elif opponent_action == "bet":
                    current_bet = opponent_bet
                    pot += opponent_bet
                    opponent_money -= opponent_bet
                    raise_count += 1
            elif action == "call" and current_bet > 0:
                if current_bet <= history['money']:
                    history["money"] -= current_bet
                    player_total_bet += current_bet
                    pot += current_bet
                    break
                else:
                    click.secho(f"Not enough money! Max bet ${history['money']}.", fg="red")
            elif action.startswith("bet ") and current_bet == 0:
                try:
                    amount = int(action.split()[1])
                    if amount > 0 and amount <= history['money']:
                        history["money"] -= amount
                        player_total_bet += amount
                        pot += amount
                        current_bet = amount
                        raise_count += 1
                        opponent_action, opponent_bet = game.opponent_action(current_bet, pot, "flop", opponent_hole, community_cards[:3], opponent_money, raise_count, history["money"])
                        click.secho(f"Opponent: {opponent_action.capitalize()} ${opponent_bet}", fg="yellow")
                        if opponent_action == "fold":
                            history["wins"] += 1
                            history["money"] += pot
                            click.secho(f"Opponent folds! {name} wins ${pot}.", fg="green")
                            break
                        elif opponent_action == "call":
                            pot += opponent_bet
                            opponent_money -= opponent_bet
                            break
                        elif opponent_action == "raise" and raise_count < 4:
                            current_bet = opponent_bet
                            pot += opponent_bet
                            opponent_money -= opponent_bet
                            raise_count += 1
                            if raise_count >= 4:  # Max 4 raises per street
                                break
                        else:
                            break
                    else:
                        click.secho(f"Invalid bet! Must be between 1 and ${history['money']}.", fg="red")
                except:
                    click.secho("Invalid bet format! Use 'bet <amount>'.", fg="red")
            elif action.startswith("raise ") and current_bet > 0:
                try:
                    amount = int(action.split()[1])
                    if amount >= current_bet and amount <= history['money'] and raise_count < 4:
                        history["money"] -= amount
                        player_total_bet += amount
                        pot += amount
                        current_bet = amount
                        raise_count += 1
                        opponent_action, opponent_bet = game.opponent_action(current_bet, pot, "flop", opponent_hole, community_cards[:3], opponent_money, raise_count, history["money"])
                        click.secho(f"Opponent: {opponent_action.capitalize()} ${opponent_bet}", fg="yellow")
                        if opponent_action == "fold":
                            history["wins"] += 1
                            history["money"] += pot
                            click.secho(f"Opponent folds! {name} wins ${pot}.", fg="green")
                            break
                        elif opponent_action == "call":
                            pot += opponent_bet
                            opponent_money -= opponent_bet
                            break
                        elif opponent_action == "raise" and raise_count < 4:
                            current_bet = opponent_bet
                            pot += opponent_bet
                            opponent_money -= opponent_bet
                            raise_count += 1
                            if raise_count >= 4:  # Max 4 raises per street
                                break
                        else:
                            break
                    else:
                        click.secho(f"Invalid raise! Must be between ${current_bet} and ${history['money']}.", fg="red")
                except:
                    click.secho("Invalid raise format! Use 'raise <amount>'.", fg="red")
            else:
                click.secho(f"Invalid action! Use {'check, bet <amount>, fold, or finish' if current_bet == 0 else 'call, raise <amount>, fold, or finish'}.", fg="red")
        if action == "fold" or opponent_action == "fold" or action == "finish":
            if action == "finish":
                break
            continue
        # Turn
        click.secho(f"Turn: {community_cards[3]}", fg="green")
        click.secho(f"With Turn: {', '.join(community_cards[:4])}", fg="green")
        current_bet = 0
        raise_count = 0
        while True:
            if history["money"] == 0:
                click.secho(f"{name} is all-in!", fg="yellow")
                break
            click.secho(f"Money: ${history['money']}", fg="blue")
            click.secho(f"Your cards: {cards}", fg=color)
            action_prompt = f"Turn (Pot ${pot}): Check, Bet <amount>, Fold, or Finish" if current_bet == 0 else f"Turn (Pot ${pot}): Call ${current_bet}, Raise <amount>, Fold, or Finish"
            action = click.prompt(action_prompt, type=str)
            action = action.lower().replace('$', '').strip()
            if action == "finish":
                click.secho("Game ended by player.", fg="yellow")
                break
            elif action == "fold":
                history["losses"] += 1
                click.secho(f"{name} folds! Opponent wins ${pot}.", fg="red")
                break
            elif action == "check" and current_bet == 0:
                opponent_action, opponent_bet = game.opponent_action(current_bet, pot, "turn", opponent_hole, community_cards[:4], opponent_money, raise_count, history["money"])
                click.secho(f"Opponent: {opponent_action.capitalize()} ${opponent_bet}", fg="yellow")
                if opponent_action == "fold":
                    history["wins"] += 1
                    history["money"] += pot
                    click.secho(f"Opponent folds! {name} wins ${pot}.", fg="green")
                    break
                elif opponent_action == "check":
                    break
                elif opponent_action == "bet":
                    current_bet = opponent_bet
                    pot += opponent_bet
                    opponent_money -= opponent_bet
                    raise_count += 1
            elif action == "call" and current_bet > 0:
                if current_bet <= history['money']:
                    history["money"] -= current_bet
                    player_total_bet += current_bet
                    pot += current_bet
                    break
                else:
                    click.secho(f"Not enough money! Max bet ${history['money']}.", fg="red")
            elif action.startswith("bet ") and current_bet == 0:
                try:
                    amount = int(action.split()[1])
                    if amount > 0 and amount <= history['money']:
                        history["money"] -= amount
                        player_total_bet += amount
                        pot += amount
                        current_bet = amount
                        raise_count += 1
                        opponent_action, opponent_bet = game.opponent_action(current_bet, pot, "turn", opponent_hole, community_cards[:4], opponent_money, raise_count, history["money"])
                        click.secho(f"Opponent: {opponent_action.capitalize()} ${opponent_bet}", fg="yellow")
                        if opponent_action == "fold":
                            history["wins"] += 1
                            history["money"] += pot
                            click.secho(f"Opponent folds! {name} wins ${pot}.", fg="green")
                            break
                        elif opponent_action == "call":
                            pot += opponent_bet
                            opponent_money -= opponent_bet
                            break
                        elif opponent_action == "raise" and raise_count < 4:
                            current_bet = opponent_bet
                            pot += opponent_bet
                            opponent_money -= opponent_bet
                            raise_count += 1
                            if raise_count >= 4:  # Max 4 raises per street
                                break
                        else:
                            break
                    else:
                        click.secho(f"Invalid bet! Must be between 1 and ${history['money']}.", fg="red")
                except:
                    click.secho("Invalid bet format! Use 'bet <amount>'.", fg="red")
            elif action.startswith("raise ") and current_bet > 0:
                try:
                    amount = int(action.split()[1])
                    if amount >= current_bet and amount <= history['money'] and raise_count < 4:
                        history["money"] -= amount
                        player_total_bet += amount
                        pot += amount
                        current_bet = amount
                        raise_count += 1
                        opponent_action, opponent_bet = game.opponent_action(current_bet, pot, "turn", opponent_hole, community_cards[:4], opponent_money, raise_count, history["money"])
                        click.secho(f"Opponent: {opponent_action.capitalize()} ${opponent_bet}", fg="yellow")
                        if opponent_action == "fold":
                            history["wins"] += 1
                            history["money"] += pot
                            click.secho(f"Opponent folds! {name} wins ${pot}.", fg="green")
                            break
                        elif opponent_action == "call":
                            pot += opponent_bet
                            opponent_money -= opponent_bet
                            break
                        elif opponent_action == "raise" and raise_count < 4:
                            current_bet = opponent_bet
                            pot += opponent_bet
                            opponent_money -= opponent_bet
                            raise_count += 1
                            if raise_count >= 4:  # Max 4 raises per street
                                break
                        else:
                            break
                    else:
                        click.secho(f"Invalid raise! Must be between ${current_bet} and ${history['money']}.", fg="red")
                except:
                    click.secho("Invalid raise format! Use 'raise <amount>'.", fg="red")
            else:
                click.secho(f"Invalid action! Use {'check, bet <amount>, fold, or finish' if current_bet == 0 else 'call, raise <amount>, fold, or finish'}.", fg="red")
        if action == "fold" or opponent_action == "fold" or action == "finish":
            if action == "finish":
                break
            continue
        # River
        click.secho(f"River: {community_cards[4]}", fg="green")
        click.secho(f"With River: {', '.join(community_cards)}", fg="green")
        current_bet = 0
        raise_count = 0
        while True:
            if history["money"] == 0:
                click.secho(f"{name} is all-in!", fg="yellow")
                break
            click.secho(f"Money: ${history['money']}", fg="blue")
            click.secho(f"Your cards: {cards}", fg=color)
            action_prompt = f"River (Pot ${pot}): Check, Bet <amount>, Fold, or Finish" if current_bet == 0 else f"River (Pot ${pot}): Call ${current_bet}, Raise <amount>, Fold, or Finish"
            action = click.prompt(action_prompt, type=str)
            action = action.lower().replace('$', '').strip()
            if action == "finish":
                click.secho("Game ended by player.", fg="yellow")
                break
            elif action == "fold":
                history["losses"] += 1
                click.secho(f"{name} folds! Opponent wins ${pot}.", fg="red")
                break
            elif action == "check" and current_bet == 0:
                opponent_action, opponent_bet = game.opponent_action(current_bet, pot, "river", opponent_hole, community_cards, opponent_money, raise_count, history["money"])
                click.secho(f"Opponent: {opponent_action.capitalize()} ${opponent_bet}", fg="yellow")
                if opponent_action == "fold":
                    history["wins"] += 1
                    history["money"] += pot
                    click.secho(f"Opponent folds! {name} wins ${pot}.", fg="green")
                    break
                elif opponent_action == "check":
                    break
                elif opponent_action == "bet":
                    current_bet = opponent_bet
                    pot += opponent_bet
                    opponent_money -= opponent_bet
                    raise_count += 1
            elif action == "call" and current_bet > 0:
                if current_bet <= history['money']:
                    history["money"] -= current_bet
                    player_total_bet += current_bet
                    pot += current_bet
                    break
                else:
                    click.secho(f"Not enough money! Max bet ${history['money']}.", fg="red")
            elif action.startswith("bet ") and current_bet == 0:
                try:
                    amount = int(action.split()[1])
                    if amount > 0 and amount <= history['money']:
                        history["money"] -= amount
                        player_total_bet += amount
                        pot += amount
                        current_bet = amount
                        raise_count += 1
                        opponent_action, opponent_bet = game.opponent_action(current_bet, pot, "river", opponent_hole, community_cards, opponent_money, raise_count, history["money"])
                        click.secho(f"Opponent: {opponent_action.capitalize()} ${opponent_bet}", fg="yellow")
                        if opponent_action == "fold":
                            history["wins"] += 1
                            history["money"] += pot
                            click.secho(f"Opponent folds! {name} wins ${pot}.", fg="green")
                            break
                        elif opponent_action == "call":
                            pot += opponent_bet
                            opponent_money -= opponent_bet
                            break
                        elif opponent_action == "raise" and raise_count < 4:
                            current_bet = opponent_bet
                            pot += opponent_bet
                            opponent_money -= opponent_bet
                            raise_count += 1
                            if raise_count >= 4:  # Max 4 raises per street
                                break
                        else:
                            break
                    else:
                        click.secho(f"Invalid bet! Must be between 1 and ${history['money']}.", fg="red")
                except:
                    click.secho("Invalid bet format! Use 'bet <amount>'.", fg="red")
            elif action.startswith("raise ") and current_bet > 0:
                try:
                    amount = int(action.split()[1])
                    if amount >= current_bet and amount <= history['money'] and raise_count < 4:
                        history["money"] -= amount
                        player_total_bet += amount
                        pot += amount
                        current_bet = amount
                        raise_count += 1
                        opponent_action, opponent_bet = game.opponent_action(current_bet, pot, "river", opponent_hole, community_cards, opponent_money, raise_count, history["money"])
                        click.secho(f"Opponent: {opponent_action.capitalize()} ${opponent_bet}", fg="yellow")
                        if opponent_action == "fold":
                            history["wins"] += 1
                            history["money"] += pot
                            click.secho(f"Opponent folds! {name} wins ${pot}.", fg="green")
                            break
                        elif opponent_action == "call":
                            pot += opponent_bet
                            opponent_money -= opponent_bet
                            break
                        elif opponent_action == "raise" and raise_count < 4:
                            current_bet = opponent_bet
                            pot += opponent_bet
                            opponent_money -= opponent_bet
                            raise_count += 1
                            if raise_count >= 4:  # Max 4 raises per street
                                break
                        else:
                            break
                    else:
                        click.secho(f"Invalid raise! Must be between ${current_bet} and ${history['money']}.", fg="red")
                except:
                    click.secho("Invalid raise format! Use 'raise <amount>'.", fg="red")
            else:
                click.secho(f"Invalid action! Use {'check, bet <amount>, fold, or finish' if current_bet == 0 else 'call, raise <amount>, fold, or finish'}.", fg="red")
        if action == "fold" or opponent_action == "fold" or action == "finish":
            if action == "finish":
                break
            continue
        # Showdown (if all-in, show remaining cards first)
        if history["money"] == 0:
            if len(community_cards[:3]) == 0:  # If all-in on preflop
                click.secho(f"Flop: {', '.join(community_cards[:3])}", fg="green")
                click.secho(f"With Flop: {', '.join(community_cards[:3])}", fg="green")
            if len(community_cards[:4]) == 3:  # If all-in on flop
                click.secho(f"Turn: {community_cards[3]}", fg="green")
                click.secho(f"With Turn: {', '.join(community_cards[:4])}", fg="green")
            if len(community_cards) == 4:  # If all-in on turn
                click.secho(f"River: {community_cards[4]}", fg="green")
                click.secho(f"With River: {', '.join(community_cards)}", fg="green")
        result = game.play(player_hole, opponent_hole, community_cards, pot, player_total_bet)
        history["bets"][f"round{i}"] = player_total_bet
        history["hands"][f"round{i}"] = {
            "player_hole": player_hole,
            "opponent_hole": opponent_hole,
            "community_cards": community_cards,
            "result": result["winner"],
            "player_rank": result["rank"],
            "opponent_rank": result["rank"] if result["winner"] == "Tie" else game.evaluate_best_hand(opponent_hole, community_cards)[0]
        }
        history["rounds"] += 1
        click.secho(f"Your hand: {player_hole} + {community_cards} -> {result['rank']}", fg="blue")
        click.secho(f"Opponent's hand: {opponent_hole} + {community_cards} -> {result['rank'] if result['winner'] == 'Tie' else game.evaluate_best_hand(opponent_hole, community_cards)[0]}", fg="blue")
        if result["winner"] == "Player":
            history["wins"] += 1
            history["money"] += pot
            click.secho(f"{name} wins ${pot} with {result['rank']}!", fg="green")
        elif result["winner"] == "Opponent":
            history["losses"] += 1
            click.secho(f"{name} loses ${-result['pot']} against Opponent's {result['rank']}!", fg="red")
        else:
            history["ties"] += 1
            click.secho("It's a tie!", fg="yellow")
    click.secho(f"Rounds: {history['rounds']}", fg="green")
    click.secho(f"Wins: {history['wins']}", fg="green")
    click.secho(f"Losses: {history['losses']}", fg="red")
    click.secho(f"Ties: {history['ties']}", fg="yellow")
    click.secho(f"Money: ${history['money']}", fg="green")
    with open("game_history.json", "w") as f:
        json.dump(history, f, indent=4)

if __name__ == "__main__":
    cli()