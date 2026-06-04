import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.preprocessing import LabelEncoder

np.random.seed(42)
n = 500
data = pd.DataFrame({
    "tenure":           np.random.randint(1, 72, n),
    "monthly_charges":  np.round(np.random.uniform(20, 120, n), 2),
    "num_products":     np.random.randint(1, 5, n),
    "has_support":      np.random.randint(0, 2, n),
    "payment_delays":   np.random.randint(0, 10, n),
    "satisfaction":     np.random.randint(1, 6, n),
})
data["churn"] = ((data["tenure"] < 12) & (data["satisfaction"] < 3) |
                 (data["payment_delays"] > 5) |
                 (data["monthly_charges"] > 100) & (data["satisfaction"] < 4)).astype(int)

X = data.drop("churn", axis=1)
y = data["churn"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

acc = model.score(X_test, y_test)

def predict_customer():
    print("\nEnter customer details:")
    tenure          = int(input("  Months as customer (e.g. 24): "))
    monthly_charges = float(input("  Monthly charges in RM (e.g. 75.50): "))
    num_products    = int(input("  Number of products subscribed (1-4): "))
    has_support     = int(input("  Has support plan? (1=yes, 0=no): "))
    payment_delays  = int(input("  Payment delays in last year (0-10): "))
    satisfaction    = int(input("  Satisfaction score (1-5): "))
    features = pd.DataFrame([[tenure, monthly_charges, num_products, has_support, payment_delays, satisfaction]],
                            columns=X.columns)
    pred  = model.predict(features)[0]
    proba = model.predict_proba(features)[0]
    risk  = proba[1] * 100
    if risk >= 70:   level = "🔴 HIGH risk"
    elif risk >= 40: level = "🟡 MEDIUM risk"
    else:            level = "🟢 LOW risk"
    print(f"\n  Churn Risk  : {risk:.1f}% — {level}")
    print(f"  Prediction  : {'Will churn ⚠️' if pred == 1 else 'Will stay ✅'}")
    if pred == 1:
        print("\n  Suggested actions:")
        if satisfaction < 3: print("    • Reach out to improve satisfaction")
        if payment_delays > 3: print("    • Offer payment plan flexibility")
        if monthly_charges > 80: print("    • Offer loyalty discount")

def main():
    print("=== Customer Churn Predictor ===")
    print(f"Model trained on {len(X_train)} customers | Accuracy: {acc*100:.1f}%")
    while True:
        print("\n1. Predict customer churn  2. View model report  3. Quit")
        c = input("Choice: ").strip()
        if c == "1": predict_customer()
        elif c == "2":
            preds = model.predict(X_test)
            print("\n" + classification_report(y_test, preds, target_names=["Stay","Churn"]))
        elif c == "3": break

if __name__ == "__main__":
    main()
