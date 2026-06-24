import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris, load_wine, load_breast_cancer
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, f1_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
import time

MODELS = {
    "Logistic Regression":     LogisticRegression(max_iter=200, random_state=42),
    "Decision Tree":           DecisionTreeClassifier(random_state=42),
    "Random Forest":           RandomForestClassifier(n_estimators=50, random_state=42),
    "Gradient Boosting":       GradientBoostingClassifier(n_estimators=50, random_state=42),
    "SVM":                     SVC(random_state=42),
    "K-Nearest Neighbors":     KNeighborsClassifier(),
    "Naive Bayes":             GaussianNB(),
}

DATASETS = {
    "1": ("Iris (flower classification)",       load_iris),
    "2": ("Wine (wine type classification)",    load_wine),
    "3": ("Breast Cancer (diagnosis)",          load_breast_cancer),
}

def compare(X, y, dataset_name):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    scaler  = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test  = scaler.transform(X_test)
    results = []
    print(f"\nTraining {len(MODELS)} models on {dataset_name}...\n")
    print(f"{'Model':<25} {'Accuracy':>10} {'F1 Score':>10} {'CV Mean':>10} {'Time':>8}")
    print("-" * 65)
    for name, model in MODELS.items():
        start  = time.time()
        model.fit(X_train, y_train)
        elapsed = time.time() - start
        preds   = model.predict(X_test)
        acc     = accuracy_score(y_test, preds)
        f1      = f1_score(y_test, preds, average="weighted")
        cv      = cross_val_score(model, X_train, y_train, cv=5).mean()
        results.append({"model": name, "accuracy": acc, "f1": f1, "cv": cv, "time": elapsed})
        print(f"{name:<25} {acc*100:>9.2f}% {f1*100:>9.2f}% {cv*100:>9.2f}% {elapsed:>7.3f}s")
    best = max(results, key=lambda x: x["accuracy"])
    print(f"\n🏆 Best model: {best['model']} ({best['accuracy']*100:.2f}% accuracy)")
    df = pd.DataFrame(results)
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    fig.suptitle(f"ML Model Comparison — {dataset_name}", fontsize=13)
    colors = plt.cm.viridis(np.linspace(0.2, 0.9, len(results)))
    axes[0].barh(df["model"], df["accuracy"]*100, color=colors)
    axes[0].set_xlabel("Accuracy (%)"); axes[0].set_title("Test Accuracy")
    axes[0].set_xlim(50, 105)
    axes[1].barh(df["model"], df["f1"]*100, color=colors)
    axes[1].set_xlabel("F1 Score (%)"); axes[1].set_title("F1 Score (weighted)")
    axes[1].set_xlim(50, 105)
    axes[2].barh(df["model"], df["time"], color=colors)
    axes[2].set_xlabel("Time (seconds)"); axes[2].set_title("Training Time")
    for ax in axes: ax.invert_yaxis()
    plt.tight_layout()
    plt.savefig("model_comparison.png", dpi=150, bbox_inches="tight")
    print("Chart saved to model_comparison.png")
    plt.show()
    return df

def main():
    print("=== ML Model Comparison Dashboard ===")
    print("\nSelect dataset:")
    for k, (name, _) in DATASETS.items():
        print(f"  {k}. {name}")
    choice = input("Choice (1-3): ").strip()
    if choice not in DATASETS:
        print("Invalid choice."); return
    name, loader = DATASETS[choice]
    data = loader()
    compare(data.data, data.target, name)

if __name__ == "__main__":
    main()
