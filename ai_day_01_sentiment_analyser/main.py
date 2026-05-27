from textblob import TextBlob

def analyse(text):
    blob       = TextBlob(text)
    polarity   = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity
    if polarity > 0.1:
        sentiment = "😊 Positive"
    elif polarity < -0.1:
        sentiment = "😞 Negative"
    else:
        sentiment = "😐 Neutral"
    return sentiment, polarity, subjectivity

def main():
    print("=== Sentiment Analyser ===")
    print("Type any text and get an instant sentiment reading.\n")
    while True:
        text = input("Enter text (or 'quit'): ").strip()
        if text.lower() == "quit":
            break
        if not text:
            continue
        sentiment, polarity, subjectivity = analyse(text)
        print(f"  Sentiment    : {sentiment}")
        print(f"  Polarity     : {polarity:.2f}  (-1=very negative, +1=very positive)")
        print(f"  Subjectivity : {subjectivity:.2f}  (0=objective, 1=very subjective)\n")

if __name__ == "__main__":
    main()
