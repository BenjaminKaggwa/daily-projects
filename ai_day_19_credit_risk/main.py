import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.preprocessing import LabelEncoder

np.random.seed(42)
n = 800

data = pd.DataFrame({
    "age":              np.random.randint(18, 70, n),
    "income":          np.random.randint(1500, 20000, n),
    "loan_amount":     np.random.randint(1000, 100000, n),
    "loan_tenure":     np.random.randint(6, 60, n),
    "existing_loans":  np.random.randint(0, 5, n),
    "credit_score":    np.random.randint(300, 850, n),
    "employment_years":np.random.randint(0, 30, n),
    "missed_payments": np.random.randint(0, 10, n),
})

def assign_risk(row):
    score = 0
    if row["credit_score"] >= 700: score += 2
    elif row["credit_score"] >= 600: score += 1
    if row["income"] / max(row["loan_amount"]/row["loan_tenure"], 1) > 3: score += 2
    elif row["income"] / max(row["loan_amount"]/row["loan_tenure"], 1) > 1.5: score += 1
    if row["missed_payments"] == 0: score += 2
    elif row["missed_payments"] <= 2: score += 1
    if row["existing_loans"] == 0: score += 1
    if row["employment_years"] >= 3: score += 1
    if score >= 7: return "Low"
    if score >= 4: return "Medium"
    return "High"

data["risk"] = data.apply(assign_risk, axis=1)
le = LabelEncoder()
X  = data.drop("risk", axis=1)
y  = le.fit_transform(data["risk"])
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = GradientBoostingClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
acc = model.score(X_test, y_test)

def assess(age, income, loan_amount, tenure, existing_loans, credit_score, emp_years, missed):
    features = pd.DataFrame([[age, income, loan_amount, tenure, existing_loans, credit_score, emp_years, missed]],
                            columns=X.columns)
    pred  = model.predict(features)[0]
    proba = model.predict_proba(features)[0]
    risk  = le.inverse_transform([pred])[0]
    return risk, dict(zip(le.classes_, proba))

def main():
    print("=== Credit Risk Classifier ===")
    print(f"Model accuracy: {acc*100:.1f}%\n")
    while True:
        print("1. Assess applicant  2. Model report  3. Quit")
        c = input("Choice: ").strip()
        if c == "1":
            try:
                age    = int(input("Age: "))
                income = float(input("Monthly income (RM): "))
                loan   = float(input("Loan amount (RM): "))
                tenure = int(input("Loan tenure (months): "))
                exist  = int(input("Existing loans: "))
                score  = int(input("Credit score (300-850): "))
                emp    = int(input("Years employed: "))
                missed = int(input("Missed payments (last 2 years): "))
                risk, proba = assess(age, income, loan, tenure, exist, score, emp, missed)
                icons = {"Low":"🟢","Medium":"🟡","High":"🔴"}
                print(f"\n  Risk Level   : {icons[risk]} {risk} Risk")
                print(f"  Probabilities:")
                for label in ["Low","Medium","High"]:
                    idx = list(le.classes_).index(label)
                    p   = proba.get(idx, 0) * 100
                    print(f"    {label:<8}: {p:.1f}%")
                monthly = loan / tenure
                dti     = monthly / income * 100
                print(f"\n  Monthly repayment : RM{monthly:.0f}")
                print(f"  Debt-to-income    : {dti:.1f}%")
            except Exception as e:
                print(f"Error: {e}")
        elif c == "2":
            preds = model.predict(X_test)
            print("\n" + classification_report(y_test, preds, target_names=le.classes_))
        elif c == "3":
            break

if __name__ == "__main__":
    main()
