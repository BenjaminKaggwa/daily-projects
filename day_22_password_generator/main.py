import random
import string
import pyperclip

def generate(length=16, use_upper=True, use_digits=True, use_symbols=True, exclude_ambiguous=True):
    chars = string.ascii_lowercase
    required = [random.choice(string.ascii_lowercase)]
    if use_upper:
        pool = string.ascii_uppercase
        if exclude_ambiguous: pool = pool.replace("O","").replace("I","")
        chars += pool
        required.append(random.choice(pool))
    if use_digits:
        pool = string.digits
        if exclude_ambiguous: pool = pool.replace("0","").replace("1","")
        chars += pool
        required.append(random.choice(pool))
    if use_symbols:
        pool = "!@#$%^&*()-_=+[]{}|;:,.<>?"
        chars += pool
        required.append(random.choice(pool))
    if exclude_ambiguous:
        chars = chars.replace("O","").replace("0","").replace("I","").replace("l","").replace("1","")
    remaining = [random.choice(chars) for _ in range(length - len(required))]
    password  = required + remaining
    random.shuffle(password)
    return "".join(password)

def strength(pwd):
    score = 0
    if len(pwd) >= 12: score += 1
    if len(pwd) >= 16: score += 1
    if any(c in string.ascii_uppercase for c in pwd): score += 1
    if any(c in string.digits for c in pwd): score += 1
    if any(c in string.punctuation for c in pwd): score += 1
    return ["","🔴 Weak","🟡 Fair","🟠 Good","🟢 Strong","🟢 Very Strong"][score]

def main():
    print("=== Password Generator ===")
    while True:
        print("\n1. Generate password  2. Generate multiple  3. Quit")
        c = input("Choice: ").strip()
        if c == "1":
            try: length = int(input("Length (default 16): ") or 16)
            except: length = 16
            upper   = input("Include uppercase? (y/n, default y): ").lower() != "n"
            digits  = input("Include digits? (y/n, default y): ").lower() != "n"
            symbols = input("Include symbols? (y/n, default y): ").lower() != "n"
            pwd = generate(length, upper, digits, symbols)
            print(f"\n🔑 Password : {pwd}")
            print(f"   Strength  : {strength(pwd)}")
            print(f"   Length    : {len(pwd)}")
        elif c == "2":
            try: n = int(input("How many? "))
            except: n = 5
            try: length = int(input("Length (default 16): ") or 16)
            except: length = 16
            print()
            for i in range(n):
                pwd = generate(length)
                print(f"  {i+1}. {pwd}  {strength(pwd)}")
        elif c == "3":
            break

if __name__ == "__main__":
    main()
