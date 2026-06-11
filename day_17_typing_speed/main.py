import time
import random

SENTENCES = [
    "The quick brown fox jumps over the lazy dog",
    "Programming is the art of telling another human what one wants the computer to do",
    "Python is a versatile language used for web development data science and automation",
    "Practice makes perfect when it comes to improving your typing speed and accuracy",
    "Software engineering requires both technical skills and clear communication",
    "Every great developer you know got there by solving problems they were unqualified to solve",
    "Clean code is not written by following a set of rules it is written by someone who cares",
    "The best way to learn programming is to build projects and solve real problems",
]

def calculate_accuracy(original, typed):
    orig_words  = original.split()
    typed_words = typed.split()
    correct = sum(1 for a, b in zip(orig_words, typed_words) if a == b)
    return (correct / len(orig_words)) * 100 if orig_words else 0

def main():
    print("=== Typing Speed Test ===")
    scores = []
    while True:
        print("\n1. Start test  2. View scores  3. Quit")
        c = input("Choice: ").strip()
        if c == "1":
            sentence = random.choice(SENTENCES)
            print(f"\nType this sentence:\n\n  {sentence}\n")
            input("Press Enter when ready...")
            print("Go!")
            start  = time.time()
            typed  = input()
            elapsed = time.time() - start
            words   = len(sentence.split())
            wpm     = int((words / elapsed) * 60)
            acc     = calculate_accuracy(sentence, typed)
            print(f"\n⏱  Time     : {elapsed:.2f} seconds")
            print(f"💨 WPM      : {wpm}")
            print(f"🎯 Accuracy : {acc:.1f}%")
            scores.append({"wpm": wpm, "accuracy": acc})
        elif c == "2":
            if not scores: print("No scores yet.")
            else:
                print(f"\n{'#':<5} {'WPM':<8} {'Accuracy'}")
                for i, s in enumerate(scores, 1):
                    print(f"{i:<5} {s['wpm']:<8} {s['accuracy']:.1f}%")
                avg_wpm = sum(s['wpm'] for s in scores) / len(scores)
                print(f"\nAverage WPM: {avg_wpm:.0f}")
        elif c == "3":
            break

if __name__ == "__main__":
    main()
