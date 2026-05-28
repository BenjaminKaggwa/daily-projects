from sklearn.datasets import load_digits
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import numpy as np

def main():
    print("=== Handwritten Digit Recogniser ===")
    print("Loading digit dataset...")
    digits = load_digits()
    X, y   = digits.data, digits.target

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    print(f"Training on {len(X_train)} samples...")
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    score  = model.score(X_test, y_test)
    preds  = model.predict(X_test)

    print(f"\n✅ Model accuracy: {score*100:.2f}%")
    print("\nClassification Report:")
    print(classification_report(y_test, preds))

    print("\nShowing sample predictions (close the window to continue)...")
    fig, axes = plt.subplots(2, 5, figsize=(12, 5))
    fig.suptitle("Handwritten Digit Recogniser — Sample Predictions", fontsize=14)
    for i, ax in enumerate(axes.flat):
        idx = np.random.randint(0, len(X_test))
        ax.imshow(X_test[idx].reshape(8, 8), cmap="gray")
        pred   = preds[idx]
        actual = y_test[idx]
        color  = "green" if pred == actual else "red"
        ax.set_title(f"Pred: {pred}\nActual: {actual}", color=color, fontsize=10)
        ax.axis("off")
    plt.tight_layout()
    plt.savefig("predictions.png")
    print("Predictions saved to predictions.png")
    plt.show()

if __name__ == "__main__":
    main()
