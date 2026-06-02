import nltk
import re
nltk.download("stopwords", quiet=True)
nltk.download("punkt", quiet=True)
nltk.download("punkt_tab", quiet=True)
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

STOPWORDS = set(stopwords.words("english"))

def clean(text):
    text = text.lower()
    text = re.sub(r"[^a-z\s]", " ", text)
    words = [w for w in text.split() if w not in STOPWORDS and len(w) > 2]
    return " ".join(words)

def score(resume, job_desc):
    cleaned = [clean(resume), clean(job_desc)]
    tfidf   = TfidfVectorizer()
    matrix  = tfidf.fit_transform(cleaned)
    sim     = cosine_similarity(matrix[0:1], matrix[1:2])[0][0]
    job_words    = set(clean(job_desc).split())
    resume_words = set(clean(resume).split())
    matched   = job_words & resume_words
    missing   = job_words - resume_words
    top_missing = sorted(missing, key=lambda w: len(w), reverse=True)[:10]
    return sim * 100, matched, top_missing

def main():
    print("=== Resume Keyword Scorer ===")
    while True:
        print("\n1. Score resume  2. Quit")
        c = input("Choice: ").strip()
        if c == "1":
            print("\nPaste your RESUME (type END when done):")
            resume_lines = []
            while True:
                l = input()
                if l.strip() == "END": break
                resume_lines.append(l)
            print("\nPaste the JOB DESCRIPTION (type END when done):")
            job_lines = []
            while True:
                l = input()
                if l.strip() == "END": break
                job_lines.append(l)
            resume   = " ".join(resume_lines)
            job_desc = " ".join(job_lines)
            sim, matched, missing = score(resume, job_desc)
            print(f"\n{'='*50}")
            if sim >= 70:   rating = "🟢 Excellent match"
            elif sim >= 50: rating = "🟡 Good match"
            elif sim >= 30: rating = "🟠 Fair match"
            else:           rating = "🔴 Poor match — add more keywords"
            print(f"  Match Score  : {sim:.1f}% — {rating}")
            print(f"  Keywords matched: {len(matched)}")
            if missing:
                print(f"\n  ⚠️  Missing keywords to add to your resume:")
                for w in missing[:10]:
                    print(f"    • {w}")
            print("="*50)
        elif c == "2":
            break

if __name__ == "__main__":
    main()
