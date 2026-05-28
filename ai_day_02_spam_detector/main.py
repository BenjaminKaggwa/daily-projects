from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# Training data — real-world style examples
EMAILS = [
    ("Win a free iPhone now! Click here to claim your prize!", "spam"),
    ("Congratulations! You have been selected for a cash reward!", "spam"),
    ("URGENT: Your account has been compromised. Verify now!", "spam"),
    ("Buy cheap medicines online. No prescription needed!", "spam"),
    ("You are the lucky winner of $1,000,000 lottery!", "spam"),
    ("Get rich quick with this simple investment trick!", "spam"),
    ("FREE credit score check — no strings attached!", "spam"),
    ("Act now! Limited time offer — 90% off all products!", "spam"),
    ("Earn money from home — no experience needed!", "spam"),
    ("Click this link to unsubscribe or you will be charged!", "spam"),
    ("Hi, can we reschedule our meeting to Thursday?", "ham"),
    ("Please find the attached report for your review.", "ham"),
    ("The project deadline has been moved to next Friday.", "ham"),
    ("Thank you for your application. We will be in touch.", "ham"),
    ("Reminder: Team standup at 10am tomorrow.", "ham"),
    ("Your order has been shipped and will arrive by Monday.", "ham"),
    ("Please review the pull request when you get a chance.", "ham"),
    ("The quarterly report is ready for your review.", "ham"),
    ("Can you send me the slides from today's presentation?", "ham"),
    ("Happy birthday! Hope you have a wonderful day.", "ham"),
    ("Your flight booking is confirmed. Check-in opens 24hrs before.", "ham"),
    ("Meeting notes from today are attached.", "ham"),
]

texts  = [e[0] for e in EMAILS]
labels = [e[1] for e in EMAILS]

X_train, X_test, y_train, y_test = train_test_split(texts, labels, test_size=0.2, random_state=42)

model = Pipeline([
    ("tfidf", TfidfVectorizer(stop_words="english")),
    ("clf",   MultinomialNB()),
])
model.fit(X_train, y_train)

def predict(text):
    result = model.predict([text])[0]
    proba  = model.predict_proba([text])[0]
    confidence = max(proba) * 100
    return result, confidence

def main():
    print("=== Spam Email Detector ===")
    print(f"Model trained on {len(X_train)} examples\n")
    while True:
        print("1. Check an email  2. Run test report  3. Quit")
        c = input("Choice: ").strip()
        if c == "1":
            text = input("Paste email text: ").strip()
            result, conf = predict(text)
            icon = "🚨 SPAM" if result == "spam" else "✅ HAM (not spam)"
            print(f"\nResult     : {icon}")
            print(f"Confidence : {conf:.1f}%\n")
        elif c == "2":
            preds = model.predict(X_test)
            print("\n" + classification_report(y_test, preds))
        elif c == "3":
            break

if __name__ == "__main__":
    main()
