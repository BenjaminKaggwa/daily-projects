import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
import matplotlib.pyplot as plt

def detect_anomalies(data, contamination=0.05):
    model  = IsolationForest(contamination=contamination, random_state=42)
    preds  = model.fit_predict(data)
    scores = model.score_samples(data)
    return preds, scores

def demo_financial():
    np.random.seed(42)
    n      = 300
    normal = np.random.normal(loc=[5000, 50], scale=[500, 5], size=(n, 2))
    anomalies = np.array([
        [25000, 120], [100, 5], [18000, 95], [50, 200], [30000, 150]
    ])
    data   = np.vstack([normal, anomalies])
    df     = pd.DataFrame(data, columns=["transaction_amount", "items_purchased"])
    preds, scores = detect_anomalies(df, contamination=0.05)
    df["anomaly"] = preds
    df["score"]   = scores
    n_anomalies   = (preds == -1).sum()
    print(f"\n  Dataset size    : {len(df)} records")
    print(f"  Anomalies found : {n_anomalies}")
    print(f"\n  Top anomalous records:")
    top = df[df["anomaly"]==-1].sort_values("score").head(5)
    print(f"  {'Amount':<15} {'Items':<10} {'Score'}")
    print("  " + "-"*35)
    for _, r in top.iterrows():
        print(f"  RM{r['transaction_amount']:<13.0f} {r['items_purchased']:<10.0f} {r['score']:.3f}")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12,5))
    normal_pts = df[df["anomaly"]==1]
    anom_pts   = df[df["anomaly"]==-1]
    ax1.scatter(normal_pts["transaction_amount"], normal_pts["items_purchased"], c="blue", alpha=0.5, label="Normal", s=20)
    ax1.scatter(anom_pts["transaction_amount"],   anom_pts["items_purchased"],   c="red",  alpha=0.8, label="Anomaly", s=80, marker="X")
    ax1.set_xlabel("Transaction Amount (RM)")
    ax1.set_ylabel("Items Purchased")
    ax1.set_title("Anomaly Detection")
    ax1.legend()
    ax2.hist(df["score"], bins=30, color="steelblue", edgecolor="white")
    ax2.axvline(df[df["anomaly"]==-1]["score"].max(), color="red", linestyle="--", label="Anomaly threshold")
    ax2.set_xlabel("Anomaly Score")
    ax2.set_ylabel("Count")
    ax2.set_title("Score Distribution")
    ax2.legend()
    plt.tight_layout()
    plt.savefig("anomaly_detection.png", dpi=150)
    print("\n  Plot saved to anomaly_detection.png")
    plt.show()

def analyse_csv():
    path = input("CSV file path: ").strip()
    try:
        df = pd.read_csv(path)
        numeric = df.select_dtypes(include=[np.number])
        if numeric.empty: print("No numeric columns found."); return
        print(f"Numeric columns: {list(numeric.columns)}")
        numeric = numeric.fillna(numeric.median())
        preds, scores = detect_anomalies(numeric)
        df["anomaly"] = ["Anomaly" if p==-1 else "Normal" for p in preds]
        df["score"]   = scores
        n_anom = (preds==-1).sum()
        print(f"\nFound {n_anom} anomalies out of {len(df)} records ({n_anom/len(df)*100:.1f}%)")
        out = path.replace(".csv","_anomalies.csv")
        df[df["anomaly"]=="Anomaly"].to_csv(out, index=False)
        print(f"Anomalous records saved to {out}")
    except Exception as e:
        print(f"Error: {e}")

def main():
    print("=== Data Anomaly Detector ===")
    while True:
        print("\n1. Run financial transaction demo  2. Analyse your CSV  3. Quit")
        c = input("Choice: ").strip()
        if c == "1": demo_financial()
        elif c == "2": analyse_csv()
        elif c == "3": break

if __name__ == "__main__":
    main()
