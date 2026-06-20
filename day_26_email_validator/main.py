import re
import csv
import sys
from pathlib import Path

PATTERN = re.compile(r'^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$')

def validate(email):
    email = email.strip().lower()
    if not email: return email, False, "Empty"
    if len(email) > 254: return email, False, "Too long"
    if not PATTERN.match(email): return email, False, "Invalid format"
    domain = email.split("@")[1]
    if ".." in domain: return email, False, "Double dot in domain"
    return email, True, "Valid"

def check_list(emails):
    valid, invalid = [], []
    print(f"\n{'Email':<40} {'Status':<10} {'Note'}")
    print("-" * 60)
    for raw in emails:
        email, ok, note = validate(raw)
        status = "✅ Valid" if ok else "❌ Invalid"
        print(f"{email:<40} {status:<10} {note}")
        (valid if ok else invalid).append(email)
    print(f"\nValid: {len(valid)}  Invalid: {len(invalid)}")
    return valid, invalid

def main():
    print("=== Email Validator ===")
    while True:
        print("\n1. Check single email  2. Check from CSV  3. Enter multiple  4. Quit")
        c = input("Choice: ").strip()
        if c == "1":
            email, ok, note = validate(input("Email: "))
            print(f"{'✅ Valid' if ok else '❌ Invalid'}: {note}")
        elif c == "2":
            fp = input("CSV file path: ").strip()
            if not Path(fp).exists(): print("File not found."); continue
            with open(fp) as f:
                emails = [row[0] for row in csv.reader(f) if row]
            valid, _ = check_list(emails)
            out = Path(fp).stem + "_valid.txt"
            Path(out).write_text("\n".join(valid))
            print(f"Valid emails saved to {out}")
        elif c == "3":
            print("Enter emails one per line. Type END to finish:")
            emails = []
            while True:
                e = input()
                if e.strip().upper() == "END": break
                emails.append(e)
            check_list(emails)
        elif c == "4": break

if __name__ == "__main__":
    main()
