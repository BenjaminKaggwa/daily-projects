import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.preprocessing import LabelEncoder

np.random.seed(42)
n = 600
roles = ["Junior Dev","Mid Dev","Senior Dev","Lead Dev","Architect","Data Analyst","Data Scientist","ML Engineer","DevOps","QA Engineer"]
education = ["Diploma","Bachelor","Master","PhD"]

data = []
for _ in range(n):
    role  = np.random.choice(roles)
    edu   = np.random.choice(education)
    exp   = np.random.randint(0, 20)
    base  = {"Junior Dev":3000,"Mid Dev":5500,"Senior Dev":8500,"Lead Dev":11000,
             "Architect":14000,"Data Analyst":5000,"Data Scientist":9000,
             "ML Engineer":10000,"DevOps":7500,"QA Engineer":4500}[role]
    edu_bonus = {"Diploma":0,"Bachelor":500,"Master":1500,"PhD":3000}[edu]
    exp_bonus = exp * 300
    noise     = np.random.normal(0, 500)
    salary    = max(2000, base + edu_bonus + exp_bonus + noise)
    data.append([role, edu, exp, salary])

df = pd.DataFrame(data, columns=["role","education","experience","salary"])
le_role = LabelEncoder()
le_edu  = LabelEncoder()
df["role_enc"] = le_role.fit_transform(df["role"])
df["edu_enc"]  = le_edu.fit_transform(df["education"])
X = df[["role_enc","edu_enc","experience"]]
y = df["salary"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = GradientBoostingRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
preds = model.predict(X_test)
mae   = mean_absolute_error(y_test, preds)
r2    = r2_score(y_test, preds)

def predict_salary(role, education, experience):
    r = le_role.transform([role])[0]
    e = le_edu.transform([education])[0]
    s = model.predict([[r, e, experience]])[0]
    return max(0, s)

def main():
    print("=== Salary Predictor ===")
    print(f"Model trained on {len(X_train)} records | MAE: RM{mae:.0f} | R²: {r2:.2f}\n")
    while True:
        print("1. Predict salary  2. View role averages  3. Quit")
        c = input("Choice: ").strip()
        if c == "1":
            print(f"\nRoles: {', '.join(roles)}")
            try:
                role = input("Role: ").strip()
                if role not in roles: print("Invalid role."); continue
                print(f"Education: {', '.join(education)}")
                edu = input("Education: ").strip()
                if edu not in education: print("Invalid education."); continue
                exp = int(input("Years of experience: "))
                salary = predict_salary(role, edu, exp)
                print(f"\n  💰 Predicted Salary: RM{salary:,.0f}/month")
                print(f"  📅 Annual: RM{salary*12:,.0f}/year")
            except Exception as e:
                print(f"Error: {e}")
        elif c == "2":
            print(f"\n{'Role':<20} {'Avg Salary (RM)'}")
            print("-"*35)
            for role in roles:
                avg = df[df["role"]==role]["salary"].mean()
                print(f"{role:<20} RM{avg:,.0f}")
        elif c == "3":
            break

if __name__ == "__main__":
    main()
