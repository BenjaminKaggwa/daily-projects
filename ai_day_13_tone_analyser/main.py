import re
import nltk
nltk.download("punkt", quiet=True)
nltk.download("punkt_tab", quiet=True)
from textblob import TextBlob
from nltk.tokenize import sent_tokenize

AGGRESSIVE = ["immediately","unacceptable","demand","furious","ridiculous","disgusting","incompetent","useless","terrible","worst","awful","pathetic","failed","failure"]
POLITE     = ["please","thank you","thanks","appreciate","kindly","would you","could you","if possible","hope","grateful","sorry","apologise"]
FORMAL     = ["dear","sincerely","regards","hereby","pursuant","enclosed","accordingly","furthermore","therefore","respectfully"]
INFORMAL   = ["hey","hi","yeah","ok","okay","gonna","wanna","lol","btw","fyi","asap","nope","yep"]

def analyse_tone(text):
    blob        = TextBlob(text)
    sentiment   = blob.sentiment.polarity
    subjectivity= blob.sentiment.subjectivity
    words       = re.findall(r"\b\w+\b", text.lower())
    agg_score   = sum(1 for w in words if w in AGGRESSIVE)
    pol_score   = sum(1 for w in words if w in POLITE)
    form_score  = sum(1 for w in words if w in FORMAL)
    inf_score   = sum(1 for w in words if w in INFORMAL)
    caps_words  = sum(1 for w in text.split() if w.isupper() and len(w) > 2)
    excl        = text.count("!")
    sents       = sent_tokenize(text)
    avg_len     = sum(len(s.split()) for s in sents) / len(sents) if sents else 0
    tones = []
    if agg_score > 0 or caps_words > 1: tones.append("😠 Aggressive")
    if pol_score > 1:                   tones.append("😊 Polite")
    if form_score > 0:                  tones.append("👔 Formal")
    if inf_score > 0:                   tones.append("😎 Informal")
    if sentiment > 0.2:                 tones.append("😄 Positive")
    elif sentiment < -0.2:              tones.append("😞 Negative")
    else:                               tones.append("😐 Neutral")
    if not tones: tones = ["📝 Neutral/Professional"]
    suggestions = []
    if agg_score > 0:
        suggestions.append("Consider softening aggressive words")
    if caps_words > 1:
        suggestions.append("Avoid excessive CAPS — it reads as shouting")
    if excl > 2:
        suggestions.append("Too many exclamation marks — reduce to 1 or 2")
    if avg_len > 30:
        suggestions.append("Some sentences are very long — consider breaking them up")
    if pol_score == 0:
        suggestions.append("Adding 'please' or 'thank you' improves reception")
    return tones, sentiment, subjectivity, suggestions, agg_score, pol_score

def main():
    print("=== Email Tone Analyser ===")
    while True:
        print("\n1. Analyse email  2. Quit")
        c = input("Choice: ").strip()
        if c == "1":
            print("Paste your email (type END on new line when done):")
            lines = []
            while True:
                l = input()
                if l.strip() == "END": break
                lines.append(l)
            text = "\n".join(lines)
            tones, sentiment, subjectivity, suggestions, agg, pol = analyse_tone(text)
            print(f"\n{'='*50}")
            print(f"  Detected Tone(s) : {', '.join(tones)}")
            print(f"  Sentiment        : {sentiment:+.2f}")
            print(f"  Subjectivity     : {subjectivity:.2f}")
            print(f"  Aggressive words : {agg}")
            print(f"  Polite words     : {pol}")
            if suggestions:
                print(f"\n  💡 Suggestions:")
                for s in suggestions:
                    print(f"     • {s}")
            print("="*50)
        elif c == "2":
            break

if __name__ == "__main__":
    main()
