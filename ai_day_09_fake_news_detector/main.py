from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
import re

TRAINING = [
    ("Scientists confirm vaccine prevents disease with 95% efficacy in peer-reviewed study", "real"),
    ("Government releases annual economic report showing 3% GDP growth", "real"),
    ("University researchers publish findings on climate change in Nature journal", "real"),
    ("Local council approves new infrastructure budget after public consultation", "real"),
    ("Central bank raises interest rates by 0.25% to combat inflation", "real"),
    ("Health ministry reports decline in dengue cases this quarter", "real"),
    ("Election commission announces voter registration deadline next month", "real"),
    ("Tech company reports quarterly earnings beat analyst expectations", "real"),
    ("SHOCKING: Government SECRETLY putting chemicals in water to control minds!!!", "fake"),
    ("DOCTORS DON'T WANT YOU TO KNOW this one weird trick cures all diseases!", "fake"),
    ("BREAKING: Celebrity admits to being part of secret global conspiracy!", "fake"),
    ("Scientists ADMIT they have been LYING about everything for decades!", "fake"),
    ("This MIRACLE food destroys cancer cells — Big Pharma is hiding it!", "fake"),
    ("EXPOSED: The truth they are desperately trying to hide from you!", "fake"),
    ("Share this NOW before they delete it — the truth is coming out!", "fake"),
    ("You won't BELIEVE what they found — mainstream media won't report this!", "fake"),
]

texts  = [t[0] for t in TRAINING]
labels = [t[1] for t in TRAINING]

model = Pipeline([
    ("tfidf", TfidfVectorizer(ngram_range=(1,2), stop_words="english")),
    ("clf",   LogisticRegression(random_state=42)),
])
model.fit(texts, labels)

def analyse(text):
    pred   = model.predict([text])[0]
    proba  = model.predict_proba([text])[0]
    conf   = max(proba) * 100
    caps   = sum(1 for w in text.split() if w.isupper() and len(w) > 2)
    excl   = text.count("!")
    red_flags = []
    if caps > 2:  red_flags.append(f"{caps} ALL CAPS words")
    if excl > 1:  red_flags.append(f"{excl} exclamation marks")
    if any(w in text.lower() for w in ["secret","they don't want","shocking","exposed","miracle"]):
        red_flags.append("Sensationalist language detected")
    return pred, conf, red_flags

def main():
    print("=== Fake News Detector ===")
    print("⚠️  Educational tool — always verify news from primary sources\n")
    while True:
        print("1. Analyse headline/text  2. Quit")
        c = input("Choice: ").strip()
        if c == "1":
            text = input("\nPaste news headline or text: ").strip()
            pred, conf, flags = analyse(text)
            icon = "✅ Likely REAL" if pred == "real" else "🚨 Likely FAKE"
            print(f"\n  Result     : {icon}")
            print(f"  Confidence : {conf:.1f}%")
            if flags:
                print(f"  Red flags  :")
                for f in flags:
                    print(f"    ⚠️  {f}")
            print()
        elif c == "2":
            break

if __name__ == "__main__":
    main()
