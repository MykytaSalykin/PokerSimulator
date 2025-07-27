# Poker Simulator
A Python-based CLI poker hand simulator that deals, evaluates, and compares poker hands, with betting and interactive gameplay.

## Features
- Generate and shuffle a standard 52-card deck.
- Deal poker hands (5 cards).
- Evaluate poker hands (Royal Flush, Straight, etc.).
- Compare two hands to determine the winner.
- Interactive mode with betting and game history.
- Display hand probabilities and rankings.

## Installation
1. Clone the repository:
   git clone https://github.com/yourusername/PokerSimulator.git
   cd PokerSimulator

2. Create and activate a virtual environment:
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate

3. Install necessary dependencies:
   pip install -r requirements.txt

Usage:
   Run the CLI with: python -m src.cli

Commands:
   Info: 
   Display poker hand rankings and optional probabilities:
   python -m src.cli info
   python -m src.cli info --probability

Deal: 
   Deal a specified number of hands: 
   python -m src.cli deal --hands 2

Play: 
   Play a single hand against the computer with a bet:
   python -m src.cli play --name Player --bet 10

Interactive: 
   Play multiple rounds with betting and track history:
   python -m src.cli interactive --name Player --rounds 3 --money 100

Requirements:
   Python 3.8+
   click==8.1.7
   pytest==8.3.3

License:
MIT License