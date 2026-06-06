import random
import re
from collections import defaultdict

CORPUS = """
The quick brown fox jumps over the lazy dog. The dog barked at the fox.
Python is a programming language that is easy to learn and powerful to use.
Machine learning is a subset of artificial intelligence that enables computers to learn from data.
Data science involves extracting knowledge and insights from structured and unstructured data.
Deep learning uses neural networks with many layers to model complex patterns in data.
Software engineering is the process of designing building and maintaining software systems.
Computer science is the study of algorithms data structures programming languages and systems.
The best way to learn programming is to build real projects and solve real problems every day.
Artificial intelligence is transforming industries including healthcare finance and education.
Natural language processing helps computers understand interpret and generate human language.
A good programmer writes code that is clean readable maintainable and well tested.
Version control systems like Git help developers track changes and collaborate on code.
Databases store and organise data so applications can retrieve and manipulate it efficiently.
Web development involves building websites and web applications for the internet.
Cybersecurity protects computer systems and networks from digital attacks and data breaches.
"""

def build_model(text, order=2):
    words = re.findall(r"\b\w+\b", text.lower())
    model = defaultdict(list)
    for i in range(len(words) - order):
        key = tuple(words[i:i+order])
        model[key].append(words[i+order])
    return model

def predict_next(model, words, order=2, n=5):
    key = tuple(words[-order:])
    if key not in model:
        return []
    candidates = model[key]
    unique = list(set(candidates))
    random.shuffle(unique)
    return unique[:n]

def autocomplete(model, seed_text, order=2, length=10):
    words = re.findall(r"\b\w+\b", seed_text.lower())
    result = list(words)
    for _ in range(length):
        if len(result) < order: break
        nexts = predict_next(model, result, order)
        if not nexts: break
        result.append(random.choice(nexts))
    return " ".join(result)

def main():
    print("=== Autocomplete Text Predictor ===")
    print("Building language model from corpus...\n")
    model = build_model(CORPUS, order=2)
    print(f"Model built with {len(model)} unique word patterns\n")
    while True:
        print("1. Predict next words  2. Autocomplete sentence  3. Quit")
        c = input("Choice: ").strip()
        if c == "1":
            text  = input("Type a few words: ").strip()
            words = re.findall(r"\b\w+\b", text.lower())
            nexts = predict_next(model, words)
            if nexts:
                print(f"  Suggestions: {', '.join(nexts)}")
            else:
                print("  No predictions — try different words from the corpus")
        elif c == "2":
            seed   = input("Starting text: ").strip()
            try: n = int(input("Words to generate (default 10): ") or 10)
            except: n = 10
            result = autocomplete(model, seed, length=n)
            print(f"\n  {result}\n")
        elif c == "3":
            break

if __name__ == "__main__":
    main()
