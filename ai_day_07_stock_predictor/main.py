import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

def get_features(df):
    df = df.copy()
    df["Return"]    = df["Close"].pct_change()
    df["MA5"]       = df["Close"].rolling(5).mean()
    df["MA20"]      = df["Close"].rolling(20).mean()
    df["Volatility"]= df["Return"].rolling(5).std()
    df["MA_diff"]   = df["MA5"] - df["MA20"]
    df["Target"]    = (df["Return"].shift(-1) > 0).astype(int)
    df.dropna(inplace=True)
    return df

def train(ticker):
    print(f"Downloading data for {ticker}...")
    raw = yf.download(ticker, period="2y", progress=False)
    if raw.empty:
        print("No data found. Check the ticker symbol.")
        return None, None, None
    df = get_features(raw)
    features = ["Return","MA5","MA20","Volatility","MA_diff"]
    X = df[features]
    y = df["Target"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    acc = accuracy_score(y_test, model.predict(X_test))
    return model, df, acc

def main():
    print("=== Stock Price Predictor ===")
    print("⚠️  For educational purposes only — not financial advice\n")
    while True:
        print("1. Predict stock  2. Quit")
        c = input("Choice: ").strip()
        if c == "1":
            ticker = input("Stock ticker (e.g. AAPL, TSLA, MSFT): ").upper()
            model, df, acc = train(ticker)
            if model is None: continue
            latest   = df[["Return","MA5","MA20","Volatility","MA_diff"]].iloc[-1:]
            pred     = model.predict(latest)[0]
            proba    = model.predict_proba(latest)[0]
            direction = "📈 UP" if pred == 1 else "📉 DOWN"
            conf     = max(proba) * 100
            price    = df["Close"].iloc[-1]
            print(f"\n  Ticker          : {ticker}")
            print(f"  Latest price    : ${float(price):.2f}")
            print(f"  Prediction      : {direction} tomorrow")
            print(f"  Confidence      : {conf:.1f}%")
            print(f"  Model accuracy  : {acc*100:.1f}% (on test data)")
        elif c == "2":
            break

if __name__ == "__main__":
    main()
