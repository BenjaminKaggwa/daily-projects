import re
import nltk
nltk.download("stopwords", quiet=True)
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords

STOPWORDS = list(stopwords.words("english"))

def clean(text):
    text = text.lower()
    text = re.sub(r"[^a-z\s]"," ",text)
    return " ".join(w for w in text.split() if len(w) > 2)

def check(doc1, doc2):
    cleaned = [clean(doc1), clean(doc2)]
    tfidf   = TfidfVectorizer(stop_words="english", ngram_range=(1,2))
    matrix  = tfidf.fit_transform(cleaned)
    sim     = cosine_similarity(matrix[0:1], matrix[1:2])[0][0] * 100
    words1  = set(clean(doc1).split())
    words2  = set(clean(doc2).split())
    common  = words1 & words2
    return sim, common

def interpret(score):
    if score >= 80: return "🔴 Very high similarity — likely plagiarised"
    if score >= 60: return "🟠 High similarity — significant overlap"
    if score >= 40: return "🟡 Moderate similarity — some shared content"
    if score >= 20: return "🟢 Low similarity — mostly original"
    return "✅ Very low similarity — original content"

def main():
    print("=== Plagiarism Checker ===")
    while True:
        print("\n1. Compare two texts  2. Compare two files  3. Quit")
        c = input("Choice: ").strip()
        if c == "1":
            print("\nPaste DOCUMENT 1 (type END when done):")
            d1 = []
            while True:
                l = input()
                if l.strip()=="END": break
                d1.append(l)
            print("Paste DOCUMENT 2 (type END when done):")
            d2 = []
            while True:
                l = input()
                if l.strip()=="END": break
                d2.append(l)
            sim, common = check(" ".join(d1), " ".join(d2))
            print(f"\n  Similarity Score : {sim:.1f}%")
            print(f"  Verdict          : {interpret(sim)}")
            print(f"  Common keywords  : {len(common)}")
            if common:
                sample = list(common)[:10]
                print(f"  Shared words     : {', '.join(sample)}")
        elif c == "2":
            f1 = input("File 1 path: ").strip()
            f2 = input("File 2 path: ").strip()
            try:
                d1 = open(f1).read()
                d2 = open(f2).read()
                sim, common = check(d1, d2)
                print(f"\n  Similarity : {sim:.1f}% — {interpret(sim)}")
            except Exception as e:
                print(f"Error: {e}")
        elif c == "3":
            break

if __name__ == "__main__":
    main()
