import random
import json
from pathlib import Path

FILE = "highscores.json"

def load_scores():
    return json.loads(Path(FILE).read_text()) if Path(FILE).exists() else []

def save_score(name, attempts, difficulty):
    scores = load_scores()
    scores.append({"name": name, "attempts": attempts, "difficulty": difficulty})
    scores.sort(key=lambda x: x["attempts"])
    Path(FILE).write_text(json.dumps(scores[:10], indent=2))

def hint(guess, target):
    diff = abs(guess - target)
    if diff == 0:   return "🎯 Correct!"
    if diff <= 5:   return "🔥 Very hot!"
    if diff <= 15:  return "♨️  Hot"
    if diff <= 30:  return "🌡  Warm"
    if diff <= 50:  return "❄️  Cold"
    return "🧊 Very cold!"

def play():
    print("\nDifficulty: 1) Easy (1-50)  2) Medium (1-100)  3) Hard (1-200)")
    d = input("Choose: ").strip()
    ranges = {"1": (1,50), "2": (1,100), "3": (1,200)}
    lo, hi = ranges.get(d, (1,100))
    target   = random.randint(lo, hi)
    attempts = 0
    name     = input("Your name: ")
    print(f"\nGuess a number between {lo} and {hi}!")
    while True:
        try:
            guess = int(input("Guess: "))
        except ValueError:
            print("Enter a valid number."); continue
        attempts += 1
        h = hint(guess, target)
        print(h)
        if guess == target:
            print(f"\n🏆 Got it in {attempts} attempt(s)!")
            save_score(name, attempts, d)
            break

def show_scores():
    scores = load_scores()
    if not scores:
        print("No scores yet.")
        return
    print(f"\n{'Name':<15} {'Attempts':<10} {'Difficulty'}")
    print("-" * 35)
    for s in scores:
        print(f"{s['name']:<15} {s['attempts']:<10} {s['difficulty']}")

def main():
    print("=== Number Guessing Game ===")
    while True:
        print("\n1. Play  2. High Scores  3. Quit")
        c = input("Choice: ").strip()
        if c == "1": play()
        elif c == "2": show_scores()
        elif c == "3": break

if __name__ == "__main__":
    main()
