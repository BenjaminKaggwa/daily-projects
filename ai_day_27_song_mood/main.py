from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

TRAINING = [
    ("I can't stop smiling today everything is wonderful life is beautiful joy everywhere", "Happy"),
    ("Dancing in the sun laughing with friends celebration love happiness pure joy", "Happy"),
    ("Best day of my life feeling amazing so grateful wonderful blessed", "Happy"),
    ("Good vibes only sunshine rainbow happy heart full of light", "Happy"),
    ("Party all night feeling alive electric energy crowd dancing together", "Energetic"),
    ("Run faster push harder never give up champion fight win power", "Energetic"),
    ("Pump it up let's go loud music bass drop fire burning hot", "Energetic"),
    ("Adrenaline rush heart racing unstoppable force moving fast alive", "Energetic"),
    ("Miss you every day empty without you tears lonely dark nights", "Sad"),
    ("Broken heart crying rain grey clouds alone missing you forever", "Sad"),
    ("Lost without you falling apart sorrow pain heartache goodbye", "Sad"),
    ("Tears on my pillow silent house memories fade into the dark", "Sad"),
    ("Breathe deep calm quiet peace meditation still water slow", "Calm"),
    ("Gentle breeze soft morning light tranquil nature restful serenity", "Calm"),
    ("Slow down rest gentle waves peaceful silence harmony nature", "Calm"),
    ("Moonlight reflection quiet contemplation soft piano evening still", "Calm"),
    ("Angry fire burning rage injustice fight back fury storms", "Angry"),
    ("Betrayed lied to backstabbed revenge furious cannot forgive ever", "Angry"),
    ("Enough screaming shouting fists clenched outrage burning mad", "Angry"),
    ("Dark rebellion chains breaking explosive rage truth fighting back", "Angry"),
]

texts  = [t[0] for t in TRAINING]
labels = [t[1] for t in TRAINING]

model = Pipeline([
    ("tfidf", TfidfVectorizer(stop_words="english", ngram_range=(1,2))),
    ("clf",   MultinomialNB()),
])
model.fit(texts, labels)

MOOD_EMOJI = {"Happy":"😊","Energetic":"⚡","Sad":"😢","Calm":"😌","Angry":"😠"}

def classify(lyrics):
    pred  = model.predict([lyrics])[0]
    proba = model.predict_proba([lyrics])[0]
    return pred, dict(zip(model.classes_, proba))

def main():
    print("=== Song Mood Classifier ===")
    print(f"Moods: {', '.join(MOOD_EMOJI.keys())}\n")
    while True:
        print("1. Classify lyrics  2. Classify song title/description  3. Quit")
        c = input("Choice: ").strip()
        if c in ("1", "2"):
            prompt = "Paste lyrics (type END when done):" if c=="1" else "Describe the song or paste title + keywords:"
            print(prompt)
            lines = []
            while True:
                l = input()
                if l.strip()=="END": break
                lines.append(l)
            text = " ".join(lines)
            mood, scores = classify(text)
            emoji = MOOD_EMOJI.get(mood, "🎵")
            print(f"\n  {emoji} Mood: {mood}")
            print(f"\n  Confidence breakdown:")
            for m, score in sorted(scores.items(), key=lambda x: -x[1]):
                bar = "█" * int(score*20)
                print(f"  {MOOD_EMOJI[m]} {m:<12} {score*100:5.1f}%  {bar}")
            print()
        elif c == "3":
            break

if __name__ == "__main__":
    main()
