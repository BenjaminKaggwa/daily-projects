import random
import re
from collections import defaultdict

CORPUS = """
Once upon a time in a land far away there lived a brave young warrior who dreamed of adventure.
The warrior set out on a long journey through dark forests and over tall mountains seeking glory.
In the forest the warrior encountered a mysterious old wizard who offered three magical gifts.
The wizard said choose wisely for only one gift will help you on your great quest ahead.
The first gift was a sword that could cut through any obstacle blocking your path forward.
The second gift was a shield that could protect you from any danger you might face alone.
The third gift was wisdom to know which path leads to victory and which leads to defeat.
The warrior chose wisdom and the old wizard smiled knowing the choice was truly the right one.
With wisdom guiding each step the warrior found allies in unexpected places along the way.
A small village was under threat from a great shadow that spread fear across the entire land.
The shadow grew stronger each night feeding on the doubts and fears of those who lived there.
But the warrior with wisdom knew that light always overcomes darkness when courage is shown.
The warrior gathered the villagers and spoke words of hope that stirred their hearts with fire.
Together they faced the shadow with courage and the shadow fled before their united light.
The village celebrated with a great feast and the warrior was honoured as a true champion.
Years later the warrior returned home changed by the journey wiser and more compassionate.
The greatest adventure was not the battles fought but the friendships found along the way.
Every hero begins as an ordinary person who simply chose to take that first brave step forward.
The story does not end here for every ending is simply the beginning of a new great adventure.
Dreams become reality when we dare to take action despite fear uncertainty and doubt within.
"""

def build(text, order=2):
    words = re.findall(r"\b\w+\b", text.lower())
    model = defaultdict(list)
    for i in range(len(words)-order):
        key = tuple(words[i:i+order])
        model[key].append(words[i+order])
    return model, words

def generate_story(model, words, order, num_words=80, start=None):
    if start:
        seed = re.findall(r"\b\w+\b", start.lower())[-order:]
    else:
        idx  = random.randint(0, len(words)-order-1)
        seed = list(words[idx:idx+order])
    result = list(seed)
    for _ in range(num_words):
        key = tuple(result[-order:])
        if key not in model: break
        next_word = random.choice(model[key])
        result.append(next_word)
    story = " ".join(result)
    sentences = re.split(r"(?<=[.!?]) +", story)
    sentences = [s.capitalize() for s in sentences]
    return " ".join(sentences)

def main():
    print("=== AI Story Generator ===")
    model, words = build(CORPUS, order=2)
    print(f"Language model built from {len(words)} words\n")
    while True:
        print("1. Generate story  2. Generate with custom start  3. Quit")
        c = input("Choice: ").strip()
        if c == "1":
            try: n = int(input("Story length in words (default 80): ") or 80)
            except: n = 80
            print(f"\n{'='*60}")
            print(generate_story(model, words, 2, n))
            print("="*60)
        elif c == "2":
            start = input("Start your story with: ").strip()
            try: n = int(input("Words to generate (default 60): ") or 60)
            except: n = 60
            print(f"\n{'='*60}")
            print(generate_story(model, words, 2, n, start))
            print("="*60)
        elif c == "3":
            break

if __name__ == "__main__":
    main()
