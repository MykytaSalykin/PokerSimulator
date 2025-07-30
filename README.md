# Poker Simulator (Texas Hold'em)

A Python-based CLI simulator for Texas Hold'em poker, featuring hand dealing, evaluation, betting rounds (preflop, flop, turn, river), dynamic opponent behavior, and game history logging.

## Features
- Simulates Texas Hold'em with 2 pocket cards and 5 community cards (flop, turn, river).
- Supports betting rounds with `call`, `raise`, `fold`, `check`, `bet`, and `finish` actions.
- **No Limit betting**: Unlimited raises per street (no artificial caps).
- **Minimum raise enforcement**: Raises must be at least the size of the previous raise (unless going all-in).
- Dynamic opponent behavior: bets, raises, or folds based on hand strength, pot odds, and randomness, with bets limited to player's available money.
- Includes small and big blinds ($1/$2).
- Evaluates hands using standard poker rankings (Royal Flush to High Card) with proper kicker comparison for tie-breakers.
- Interactive mode with balance validation ($10–$1000), bet validation (positive bets, raises ≥ current bet), and all-in handling.
- Shows pocket cards and current balance before each action in interactive mode.
- Displays community cards after flop ("With Flop"), turn ("With Turn"), and river ("With River") for clarity.
- Immediate showdown after all-in: remaining cards are revealed without further betting.
- `finish` command to exit interactive mode early, saving game history.
- Displays flop in `deal` command for transparency.
- Saves game history to `game_history.json` with bets, hands, and results for analysis.
- Includes unit tests for deck, hand evaluation, and opponent behavior.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/MykytaSalykin/PokerSimulator.git
   cd PokerSimulator
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
Run the CLI with:
```bash
python -m src.cli
```

## Commands

**Info**: Display poker hand rankings and optional probabilities:
```bash
python -m src.cli info
python -m src.cli info --probability

Example output:
Royal Flush: 10 - 0.0002% - 1 in 649,740
Straight Flush: 9 - 0.0014% - 1 in 72,193
Four of a Kind: 8 - 0.0240% - 1 in 4,165
...
```

**Deal**: Deal pocket cards for specified number of players (shows flop for example):
```bash
python -m src.cli deal --hands 2

Example output:
Your cards: AH, KH
Flop: 10H, JH, QH
Hand Rank (with flop): Royal Flush
Your cards: 2C, 3D
Flop: 10H, JH, QH
Hand Rank (with flop): High Card
```

**Play**: Play a single hand against the computer with a fixed bet:
```bash
python -m src.cli play --name Nikita --bet 10

Example output:
Your cards: AH, KH
Flop: 10H, JH, QH
Turn: 2C
With Turn: 10H, JH, QH, 2C
River: 3D
With River: 10H, JH, QH, 2C, 3D
Your hand: ['AH', 'KH'] + ['10H', 'JH', 'QH', '2C', '3D'] -> Royal Flush
Opponent's hand: ['2C', '3D'] + ['10H', 'JH', 'QH', '2C', '3D'] -> High Card
Nikita wins $20 with Royal Flush!
```

**Interactive**: Play multiple rounds with betting rounds (preflop, flop, turn, river):
```bash
python -m src.cli interactive --name Nikita --rounds 3 --money 100

Example output:
Round 1: Money: $100
Blinds: Small Blind $1, Big Blind $2 (deducted)
Your cards: 5H, 10C
Money: $98
Your cards: 5H, 10C
Pre-flop (Pot $3): Call $2, Raise <amount>, Fold, or Finish: call
Opponent: Call $2
Flop: 2D, 10D, 10H
With Flop: 2D, 10D, 10H
Money: $96
Your cards: 5H, 10C
Flop (Pot $7): Check, Bet <amount>, Fold, or Finish: bet 10
Opponent: Call $10
Turn: QD
With Turn: 2D, 10D, 10H, QD
Money: $86
Your cards: 5H, 10C
Turn (Pot $27): Check, Bet <amount>, Fold, or Finish: check
Opponent: Check $0
River: 3S
With River: 2D, 10D, 10H, QD, 3S
Money: $86
Your cards: 5H, 10C
River (Pot $27): Check, Bet <amount>, Fold, or Finish: check
Opponent: Check $0
Your hand: ['5H', '10C'] + ['2D', '10D', '10H', 'QD', '3S'] -> Three of a Kind
Opponent's hand: ['AC', 'KC'] + ['2D', '10D', '10H', 'QD', '3S'] -> One Pair
Nikita wins $27 with Three of a Kind!
...
Rounds: 3
Wins: 2
Losses: 1
Ties: 0
Money: $115
```

## Betting Rules

- **No Limit**: No artificial cap on the number of raises per street
- **Minimum Raise**: A raise must be at least the size of the previous raise (unless going all-in)
- **Blinds**: Small blind ($1) and big blind ($2) are posted automatically
- **All-in**: Players can bet their entire stack at any time
- **Call/Check**: Call when there's a bet, check when there's no bet to call

## Testing
Run unit tests to verify deck, hand evaluation, and opponent behavior:
```bash
pytest tests/
```

## Requirements
- Python 3.8+
- click==8.1.7
- colorama==0.4.6
- iniconfig==2.1.0
- packaging==25.0
- pytest==8.3.3

## License
MIT License