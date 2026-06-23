import re
import nltk
nltk.download("punkt", quiet=True)
nltk.download("punkt_tab", quiet=True)
from textblob import TextBlob

EMOTION_WORDS = {
    "joy":       ["happy","joy","excited","wonderful","amazing","love","great","fantastic","thrilled","elated","delighted","cheerful","glad"],
    "sadness":   ["sad","crying","depressed","lonely","miserable","heartbroken","grief","sorry","upset","disappointed","unhappy","gloomy"],
    "anger":     ["angry","furious","hate","rage","annoyed","frustrated","outraged","mad","livid","irritated","disgusted","infuriated"],
    "fear":      ["scared","afraid","terrified","anxious","worried","nervous","panic","dread","frightened","uneasy","apprehensive"],
    "surprise":  ["wow","shocked","surprised","unexpected","unbelievable","astonished","amazed","incredible","cant believe","omg"],
    "disgust":   ["disgusting","gross","awful","horrible","nasty","revolting","repulsive","sick","yuck","eww","terrible"],
    "trust":     ["trust","believe","confident","reliable","sure","certain","faith","honest","loyal","dependable"],
    "anticipation":["excited","looking forward","cant wait","hopeful","eager","anticipate","expect","soon","planning"],
}

EMOJI_MAP = {
    "joy":"😊","sadness":"😢","anger":"😠","fear":"😨",
    "surprise":"😲","disgust":"🤢","trust":"🤝","anticipation":"🤩"
}

def detect_emotions(text):
    words  = re.findall(r"\b\w+\b", text.lower())
    scores = {e: 0 for e in EMOTION_WORDS}
    for emotion, keywords in EMOTION_WORDS.items():
        for w in words:
            if w in keywords:
                scores[emotion] += 1
    blob      = TextBlob(text)
    polarity  = blob.sentiment.polarity
    if polarity > 0.3 and scores["joy"] == 0:   scores["joy"] += 1
    if polarity < -0.3 and scores["sadness"] == 0: scores["sadness"] += 1
    total     = sum(scores.values())
    dominant  = max(scores, key=scores.get) if total > 0 else "neutral"
    return scores, dominant, polarity, total

def main():
    print("=== Chat Emotion Detector ===")
    print("Type messages and see emotions detected in real time.\n")
    history = []
    while True:
        msg = input("You: ").strip()
        if msg.lower() in ("quit","exit","bye"):
            print("\nSession summary:")
            if history:
                from collections import Counter
                counts = Counter(h["dominant"] for h in history)
                print(f"  Messages analysed : {len(history)}")
                print(f"  Most common emotion: {counts.most_common(1)[0][0]} {EMOJI_MAP.get(counts.most_common(1)[0][0],'')}")
                print(f"  Emotion breakdown:")
                for emotion, count in counts.most_common():
                    print(f"    {EMOJI_MAP.get(emotion,'')} {emotion}: {count} message(s)")
            break
        if not msg: continue
        scores, dominant, polarity, total = detect_emotions(msg)
        history.append({"msg": msg, "dominant": dominant, "polarity": polarity})
        if total == 0:
            print(f"Bot: [😐 Neutral] I detect a neutral tone in your message.\n")
        else:
            active = [(e,s) for e,s in scores.items() if s > 0]
            active.sort(key=lambda x: -x[1])
            emotion_str = ", ".join(f"{EMOJI_MAP[e]} {e}" for e,s in active[:3])
            print(f"Bot: [{emotion_str}] Sentiment: {polarity:+.2f}\n")

if __name__ == "__main__":
    main()
