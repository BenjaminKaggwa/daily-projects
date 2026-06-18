import random
import re
from collections import defaultdict

POETRY_CORPUS = """
the golden sun sets over the quiet hills at evening time
soft light falls on the river like whispers of an old dream
the stars awaken one by one in the deep blue canvas above
a lone bird calls across the silent valley in the dusk
the wind moves through tall grass like memory through the mind
morning comes with silver light across the ancient mountain stone
the moon casts shadows long and deep across the sleeping earth
rain speaks to the roof at night in its old familiar tongue
time moves like water always forward never looking to return
the heart knows paths the eyes have never seen or walked upon
beneath the oak the old man sits and watches clouds drift by
two roads divide the forest and a choice must now be made
seasons turn like pages in a book of years gone by too fast
the sea remembers every shore it touched and every stone
love is the quiet fire that warms the coldest winter night
words are birds that fly beyond the reach of those who spoke them
the river asks no questions as it journeys to the open sea
a flower blooms in silence and asks nothing of the world
truth lives in simple things the light on water morning air
we are the stories that we tell ourselves in darkened rooms
"""

def build_model(text, order=1):
    words = re.findall(r"\b\w+\b", text.lower())
    model = defaultdict(list)
    for i in range(len(words)-order):
        key = tuple(words[i:i+order])
        model[key].append(words[i+order])
    return model, words

def generate_line(model, words, order, length=8):
    start = random.randint(0, len(words)-order-1)
    line  = list(words[start:start+order])
    for _ in range(length):
        key = tuple(line[-order:])
        if key not in model: break
        line.append(random.choice(model[key]))
    return " ".join(line)

def generate_poem(model, words, order, num_lines=4, line_length=8, title=None):
    poem = []
    if title:
        poem.append(title.upper())
        poem.append("")
    for _ in range(num_lines):
        line = generate_line(model, words, order, line_length)
        poem.append(line.capitalize())
    return "\n".join(poem)

def main():
    print("=== AI Poem Generator ===")
    model, words = build_model(POETRY_CORPUS, order=2)
    while True:
        print("\n1. Generate poem  2. Generate haiku  3. Custom poem  4. Quit")
        c = input("Choice: ").strip()
        if c == "1":
            title = input("Poem title (optional): ").strip() or None
            print(f"\n{'='*50}")
            print(generate_poem(model, words, 2, num_lines=6, line_length=9, title=title))
            print("="*50)
        elif c == "2":
            print(f"\n{'='*50}")
            print("HAIKU\n")
            for length in [5, 7, 5]:
                print(generate_line(model, words, 2, length).capitalize())
            print("="*50)
        elif c == "3":
            try:
                lines  = int(input("Number of lines (2-12): ") or 4)
                length = int(input("Words per line (5-15): ") or 8)
                title  = input("Title (optional): ").strip() or None
                print(f"\n{'='*50}")
                print(generate_poem(model, words, 2, lines, length, title))
                print("="*50)
            except: print("Invalid input.")
        elif c == "4":
            break

if __name__ == "__main__":
    main()
