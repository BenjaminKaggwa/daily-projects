import os
import re
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

SAMPLE_DOCS = {
    "doc1_python_tutorial.txt":     "Python is a high-level programming language. Python is easy to learn and widely used in data science machine learning and web development. Python has simple syntax and powerful libraries.",
    "doc2_python_basics.txt":       "Python programming is beginner friendly. The Python language supports object oriented and functional programming. Python is popular for automation scripting and data analysis.",
    "doc3_machine_learning.txt":    "Machine learning is a subset of artificial intelligence. Machine learning algorithms learn from data to make predictions. Deep learning and neural networks are advanced machine learning techniques.",
    "doc4_data_science.txt":        "Data science combines statistics programming and domain knowledge. Data scientists use Python and R to analyse large datasets. Machine learning is a core skill in data science.",
    "doc5_web_development.txt":     "Web development involves building websites and web applications. Frontend development uses HTML CSS and JavaScript. Backend development involves servers databases and APIs.",
    "doc6_cybersecurity.txt":       "Cybersecurity protects systems from digital attacks and data breaches. Security professionals use tools to detect and prevent intrusions. Encryption and firewalls are fundamental security measures.",
}

def create_samples():
    for name, content in SAMPLE_DOCS.items():
        Path(name).write_text(content)
    print(f"Created {len(SAMPLE_DOCS)} sample documents")

def load_docs(folder="."):
    docs, names = [], []
    for f in Path(folder).glob("*.txt"):
        try:
            docs.append(f.read_text())
            names.append(f.name)
        except: pass
    return docs, names

def find_similar(docs, names, threshold=0.1):
    tfidf  = TfidfVectorizer(stop_words="english")
    matrix = tfidf.fit_transform(docs)
    sim    = cosine_similarity(matrix)
    pairs  = []
    for i in range(len(names)):
        for j in range(i+1, len(names)):
            if sim[i][j] >= threshold:
                pairs.append((names[i], names[j], sim[i][j]))
    return sorted(pairs, key=lambda x: -x[2]), sim, names

def main():
    print("=== Document Similarity Finder ===")
    while True:
        print("\n1. Create sample docs & analyse  2. Analyse folder  3. Compare two texts  4. Quit")
        c = input("Choice: ").strip()
        if c == "1":
            create_samples()
            docs, names = load_docs()
            pairs, sim, names = find_similar(docs, names)
            print(f"\nAnalysed {len(docs)} documents")
            print(f"\n{'Document A':<35} {'Document B':<35} {'Similarity'}")
            print("-"*80)
            for a, b, s in pairs:
                bar = "█" * int(s*20)
                print(f"{a:<35} {b:<35} {s*100:.1f}%  {bar}")
        elif c == "2":
            folder = input("Folder path (. for current): ").strip() or "."
            docs, names = load_docs(folder)
            if len(docs) < 2: print("Need at least 2 .txt files."); continue
            pairs, _, _ = find_similar(docs, names)
            print(f"\nFound {len(pairs)} similar pairs:")
            for a, b, s in pairs:
                print(f"  {a} ↔ {b}: {s*100:.1f}%")
        elif c == "3":
            print("Paste TEXT 1 (type END when done):")
            t1 = []
            while True:
                l=input()
                if l.strip()=="END": break
                t1.append(l)
            print("Paste TEXT 2 (type END when done):")
            t2 = []
            while True:
                l=input()
                if l.strip()=="END": break
                t2.append(l)
            tfidf  = TfidfVectorizer(stop_words="english")
            matrix = tfidf.fit_transform([" ".join(t1), " ".join(t2)])
            sim    = cosine_similarity(matrix)[0][1]
            print(f"\n  Similarity: {sim*100:.1f}%")
        elif c == "4":
            break

if __name__ == "__main__":
    main()
