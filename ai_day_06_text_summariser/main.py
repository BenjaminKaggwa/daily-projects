import nltk
import re
from collections import defaultdict
nltk.download("punkt", quiet=True)
nltk.download("stopwords", quiet=True)
nltk.download("punkt_tab", quiet=True)
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords

STOPWORDS = set(stopwords.words("english"))

def summarise(text, num_sentences=3):
    sentences = sent_tokenize(text)
    if len(sentences) <= num_sentences:
        return text
    words = word_tokenize(text.lower())
    freq  = defaultdict(int)
    for w in words:
        if w.isalpha() and w not in STOPWORDS:
            freq[w] += 1
    max_freq = max(freq.values()) if freq else 1
    for w in freq:
        freq[w] /= max_freq
    scores = defaultdict(float)
    for i, sent in enumerate(sentences):
        for w in word_tokenize(sent.lower()):
            if w in freq:
                scores[i] += freq[w]
    ranked = sorted(scores, key=scores.get, reverse=True)[:num_sentences]
    ranked.sort()
    summary = " ".join(sentences[i] for i in ranked)
    return summary

def main():
    print("=== Text Summariser ===")
    while True:
        print("\n1. Summarise text  2. Summarise from file  3. Quit")
        c = input("Choice: ").strip()
        if c == "1":
            print("Paste your text (type END on a new line when done):")
            lines = []
            while True:
                l = input()
                if l.strip() == "END": break
                lines.append(l)
            text = " ".join(lines)
            try:
                n = int(input("Number of sentences in summary (default 3): ") or 3)
            except:
                n = 3
            summary = summarise(text, n)
            orig_sents = len(sent_tokenize(text))
            print(f"\n📝 Summary ({n}/{orig_sents} sentences):")
            print(f"\n{summary}")
            reduction = (1 - len(summary)/len(text)) * 100
            print(f"\nReduced by {reduction:.0f}%")
        elif c == "2":
            fp = input("File path: ").strip()
            try:
                text = open(fp).read()
                n    = int(input("Sentences in summary: ") or 3)
                print(f"\n{summarise(text, n)}")
            except Exception as e:
                print(f"Error: {e}")
        elif c == "3":
            break

if __name__ == "__main__":
    main()
