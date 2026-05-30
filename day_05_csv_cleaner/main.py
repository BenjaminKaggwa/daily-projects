import sys
import pandas as pd
from pathlib import Path

def clean(filepath):
    print(f"Loading {filepath}...")
    df = pd.read_csv(filepath)
    original_rows = len(df)
    print(f"Rows loaded: {original_rows}")
    print(f"Columns: {list(df.columns)}")

    before_dupes = len(df)
    df = df.drop_duplicates()
    print(f"Duplicates removed: {before_dupes - len(df)}")

    null_counts = df.isnull().sum()
    print(f"\nNull values per column:\n{null_counts}")

    for col in df.columns:
        if df[col].dtype == object:
            df[col] = df[col].fillna("Unknown").str.strip().str.title()
        else:
            df[col] = df[col].fillna(df[col].median())

    output = Path(filepath).stem + "_cleaned.csv"
    df.to_csv(output, index=False)
    print(f"\nCleaned file saved as: {output}")
    print(f"Final rows: {len(df)} (removed {original_rows - len(df)} total rows)")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py yourfile.csv")
    else:
        clean(sys.argv[1])
