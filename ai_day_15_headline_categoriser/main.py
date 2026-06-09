from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

HEADLINES = [
    ("Stock markets rally as inflation data comes in lower than expected", "Finance"),
    ("Central bank cuts interest rates to boost economic growth", "Finance"),
    ("Tech giant reports record profits in fourth quarter earnings", "Finance"),
    ("Cryptocurrency prices surge after regulatory clarity announced", "Finance"),
    ("Scientists discover new treatment for Alzheimer's disease", "Science"),
    ("NASA rover finds evidence of ancient water on Mars surface", "Science"),
    ("Breakthrough in quantum computing achieves new milestone", "Science"),
    ("Researchers develop biodegradable plastic alternative from seaweed", "Science"),
    ("National football team qualifies for World Cup finals", "Sports"),
    ("Tennis star wins grand slam title in thrilling five-set match", "Sports"),
    ("Olympic gold medallist breaks world record in swimming event", "Sports"),
    ("Football club signs star striker for record transfer fee", "Sports"),
    ("Government announces new climate policy ahead of international summit", "Politics"),
    ("Opposition party wins landmark seat in by-election", "Politics"),
    ("Parliament debates new data privacy legislation this week", "Politics"),
    ("Prime minister meets foreign leaders at bilateral summit", "Politics"),
    ("New superhero film breaks box office records worldwide", "Entertainment"),
    ("Award-winning director announces trilogy sequel release date", "Entertainment"),
    ("Music streaming platform reports one billion monthly users", "Entertainment"),
    ("Celebrity couple announces engagement after two years together", "Entertainment"),
    ("Startup raises millions in funding for AI-powered healthcare app", "Technology"),
    ("Social media platform introduces new privacy controls for users", "Technology"),
    ("Electric vehicle manufacturer opens new battery factory", "Technology"),
    ("Cybersecurity firm warns of new ransomware threat targeting businesses", "Technology"),
]

texts  = [h[0] for h in HEADLINES]
labels = [h[1] for h in HEADLINES]

model = Pipeline([
    ("tfidf", TfidfVectorizer(ngram_range=(1,2), stop_words="english")),
    ("clf",   MultinomialNB()),
])
model.fit(texts, labels)
categories = sorted(set(labels))

def classify(headline):
    pred  = model.predict([headline])[0]
    proba = model.predict_proba([headline])[0]
    return pred, dict(zip(model.classes_, proba))

def main():
    print("=== News Headline Categoriser ===")
    print(f"Categories: {', '.join(categories)}\n")
    while True:
        print("1. Classify headline  2. Classify multiple  3. Quit")
        c = input("Choice: ").strip()
        if c == "1":
            h = input("Headline: ").strip()
            cat, scores = classify(h)
            print(f"\n  Category: {cat}")
            print("  Confidence:")
            for cat_name, score in sorted(scores.items(), key=lambda x: -x[1]):
                bar = "█" * int(score * 20)
                print(f"    {cat_name:<15} {score*100:5.1f}%  {bar}")
            print()
        elif c == "2":
            print("Enter headlines one per line (type END when done):")
            headlines = []
            while True:
                l = input()
                if l.strip() == "END": break
                if l.strip(): headlines.append(l.strip())
            print(f"\n{'Headline':<55} {'Category'}")
            print("-"*70)
            for h in headlines:
                cat, _ = classify(h)
                print(f"{h[:54]:<55} {cat}")
        elif c == "3":
            break

if __name__ == "__main__":
    main()
