import json
import random
from pathlib import Path

FILE = "flashcards.json"

def load():
    return json.loads(Path(FILE).read_text()) if Path(FILE).exists() else {}

def save(data):
    Path(FILE).write_text(json.dumps(data, indent=2))

def create_deck(data):
    deck = input("Deck name: ").strip()
    if deck not in data: data[deck] = []
    print(f"Adding cards to '{deck}'. Type DONE when finished.")
    while True:
        q = input("Question (or DONE): ").strip()
        if q.upper() == "DONE": break
        a = input("Answer: ").strip()
        data[deck].append({"q": q, "a": a})
    save(data)
    print(f"Deck '{deck}' saved with {len(data[deck])} cards.")

def study(data):
    if not data: print("No decks yet."); return
    print("\nAvailable decks:")
    decks = list(data.keys())
    for i, d in enumerate(decks, 1):
        print(f"  {i}. {d} ({len(data[d])} cards)")
    try: deck = decks[int(input("Choose deck #: ")) - 1]
    except: print("Invalid."); return
    cards  = random.sample(data[deck], len(data[deck]))
    score  = 0
    total  = len(cards)
    print(f"\nStudying '{deck}' — {total} cards")
    for i, card in enumerate(cards, 1):
        print(f"\nQ{i}/{total}: {card['q']}")
        input("Press Enter to reveal answer...")
        print(f"A: {card['a']}")
        correct = input("Did you get it right? (y/n): ").lower()
        if correct == "y": score += 1
    pct = score / total * 100
    print(f"\n🎉 Score: {score}/{total} ({pct:.0f}%)")
    if pct == 100: print("Perfect score! 🏆")
    elif pct >= 70: print("Good job! Keep it up.")
    else: print("Keep practising — you'll get there!")

def main():
    print("=== Flashcard Study App ===")
    data = load()
    while True:
        print("\n1. Create deck  2. Study  3. List decks  4. Quit")
        c = input("Choice: ").strip()
        if c == "1": create_deck(data); data = load()
        elif c == "2": study(data)
        elif c == "3":
            if not data: print("No decks yet.")
            else: [print(f"  • {d} ({len(cards)} cards)") for d, cards in data.items()]
        elif c == "4": break

if __name__ == "__main__":
    main()
