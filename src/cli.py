import click
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
    hands_dealt = game.deal_hands(hands)
    for hand in hands_dealt:
        for card in hand:
            color = "red" if card[-1] in ["H", "D"] else "black"
            click.secho(f"{card} ", fg=color, nl=False)
        click.echo()
        rank, _ = game.evaluator.evaluate(hand)
        click.secho(f"Hand Rank: {rank}", fg="green")

@cli.command("play")
@click.option("--name", default="Player", help="Player name")
@click.option("--bet", default=1, help="Amount to bet")
def play(name, bet):
    game = PokerGame()
    hand1, hand2 = game.deal_hands(2)
    result = game.play(hand1, hand2, bet)
    for i, hand in enumerate([hand1, hand2], 1):
        for card in hand:
            color = "red" if card[-1] in ["H", "D"] else "black"
            click.secho(f"{card} ", fg=color, nl=False)
        click.echo()
        rank, _ = game.evaluator.evaluate(hand)
        click.secho(f"Hand {i} Rank: {rank}", fg="green")
    if result["winner"] == "Hand 1":
        click.secho(f"{name} wins ${bet} with Hand 1!", fg="green")
    elif result["winner"] == "Hand 2":
        click.secho(f"{name} loses ${bet} against Hand 2!", fg="red")
    else:
        click.secho("It's a tie!", fg="yellow")

@cli.command("interactive")
@click.option("--name", default="Player", help="Player name")
@click.option("--rounds", default=1, help="Number of rounds")
@click.option("--money", default=100, help="Starting money")
def interactive(name, rounds, money):
    game = PokerGame()
    history = {
        "rounds": 0, "wins": 0, "losses": 0, "ties": 0,
        "money": money, "bets": {}, "probabilities": {}
    }
    for i in range(1, rounds + 1):
        click.secho(f"Round {i}: Money: ${history['money']}", fg="blue")
        hand1, hand2 = game.deal_hands(2)
        rank, _ = game.evaluator.evaluate(hand1)
        prob = game.get_probability(hand1)
        for card in hand1:
            color = "red" if card[-1] in ["H", "D"] else "black"
            click.secho(f"{card} ", fg=color, nl=False)
        click.echo()
        click.secho(f"Hand Rank: {rank} (Probability: {prob:.2f}%)", fg="green")
        bet = click.prompt("How much to bet?", type=int)
        result = game.play(hand1, hand2, bet)
        history["bets"][f"round{i}"] = bet
        history["probabilities"][f"round{i}"] = prob
        history["rounds"] += 1
        if result["winner"] == "Hand 1":
            history["wins"] += 1
            history["money"] += bet
            click.secho(f"{name} wins ${bet} with Hand 1!", fg="green")
        elif result["winner"] == "Hand 2":
            history["losses"] += 1
            history["money"] -= bet
            click.secho(f"{name} loses ${bet} against Hand 2!", fg="red")
        else:
            history["ties"] += 1
            click.secho("It's a tie!", fg="yellow")
    click.secho(f"Rounds: {history['rounds']}", fg="green")
    click.secho(f"Wins: {history['wins']}", fg="green")
    click.secho(f"Losses: {history['losses']}", fg="red")
    click.secho(f"Ties: {history['ties']}", fg="yellow")
    click.secho(f"Money: ${history['money']}", fg="green")