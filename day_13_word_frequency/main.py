import sys
import re
from collections import Counter
from pathlib import Path

STOPWORDS = {"the","a","an","and","or","but","in","on","at","to","for","of","with","is","it","this","that","was","are","be","as","by","from","have","had","not","you","we","they","he","she","his","her","its","our","their"}

def analyse(filepath, top_n=20):
    text = Path(filepath).read_text(encoding="utf-8", errors="ignore").lower()
    words = re.findall(r"\b[a-z]{3,}\b", text)
    filtered = [w for w in words if w not in STOPWORDS]
    total = len(words)
    unique = len(set(words))
    counter = Counter(filtered)
    print(f"\n📄 File     : {filepath}")
    print(f"📊 Total words  : {total}")
    print(f"🔤 Unique words : {unique}")
    print(f"\nTop {top_n} most frequent words (excluding common stopwords):")
    print(f"\n{'Rank':<6} {'Word':<20} {'Count':>6} {'Bar'}")
    print("-" * 50)
    for rank, (word, count) in enumerate(counter.most_common(top_n), 1):
        bar = "█" * min(count, 30)
        print(f"{rank:<6} {word:<20} {count:>6}  {bar}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py yourfile.txt")
    else:
        analyse(sys.argv[1])
