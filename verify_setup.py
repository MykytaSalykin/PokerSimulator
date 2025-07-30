#!/usr/bin/env python3
"""
Verification script for PokerSimulator project structure.
Run this before pushing to GitHub to ensure everything is set up correctly.
"""

import os
import sys
from pathlib import Path


def check_file_exists(filepath, description):
    """Check if a file exists and print status."""
    if os.path.exists(filepath):
        print(f"✅ {description}: {filepath}")
        return True
    else:
        print(f"❌ Missing {description}: {filepath}")
        return False


def check_directory_exists(dirpath, description):
    """Check if a directory exists and print status."""
    if os.path.isdir(dirpath):
        print(f"✅ {description}: {dirpath}")
        return True
    else:
        print(f"❌ Missing {description}: {dirpath}")
        return False


def main():
    """Verify the project structure."""
    print("🔍 Verifying PokerSimulator project structure...\n")

    # Required files
    required_files = [
        ("README.md", "README documentation"),
        ("LICENSE", "MIT License"),
        ("requirements.txt", "Python dependencies"),
        ("pyproject.toml", "Project configuration"),
        (".gitignore", "Git ignore rules"),
        (".github/workflows/ci.yml", "GitHub Actions CI/CD"),
    ]

    # Required source files
    source_files = [
        ("src/__init__.py", "Source package init"),
        ("src/cli.py", "CLI interface"),
        ("src/game.py", "Game logic"),
        ("src/deck.py", "Deck management"),
        ("src/hand_evaluator.py", "Hand evaluation"),
    ]

    # Required test files
    test_files = [
        ("tests/__init__.py", "Test package init"),
        ("tests/test_deck.py", "Deck tests"),
        ("tests/test_game.py", "Game tests"),
        ("tests/test_hand_evaluator.py", "Hand evaluator tests"),
    ]

    # Required directories
    required_dirs = [
        ("src", "Source code directory"),
        ("tests", "Test directory"),
        (".github", "GitHub configuration"),
        (".github/workflows", "GitHub Actions workflows"),
    ]

    all_good = True

    print("📁 Checking directories...")
    for dirpath, description in required_dirs:
        if not check_directory_exists(dirpath, description):
            all_good = False

    print("\n📄 Checking required files...")
    for filepath, description in required_files:
        if not check_file_exists(filepath, description):
            all_good = False

    print("\n🐍 Checking source files...")
    for filepath, description in source_files:
        if not check_file_exists(filepath, description):
            all_good = False

    print("\n🧪 Checking test files...")
    for filepath, description in test_files:
        if not check_file_exists(filepath, description):
            all_good = False

    print("\n" + "=" * 50)

    if all_good:
        print("🎉 All checks passed! Your project is ready for GitHub.")
        print("\n📋 Next steps:")
        print("1. git add .")
        print("2. git commit -m 'Initial commit: Texas Hold'em Poker Simulator'")
        print("3. git push origin main")
        print("\n🚀 Your project will automatically run CI/CD tests on GitHub!")
    else:
        print(
            "❌ Some checks failed. Please fix the missing files before pushing to GitHub."
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
