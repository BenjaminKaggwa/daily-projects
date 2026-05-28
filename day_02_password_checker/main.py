import re
import string

def check_strength(password):
    score = 0
    feedback = []

    if len(password) >= 8:
        score += 1
    else:
        feedback.append("Use at least 8 characters")

    if len(password) >= 12:
        score += 1
    if len(password) >= 16:
        score += 1

    if any(c in string.ascii_lowercase for c in password):
        score += 1
    else:
        feedback.append("Add lowercase letters")

    if any(c in string.ascii_uppercase for c in password):
        score += 1
    else:
        feedback.append("Add uppercase letters")

    if any(c in string.digits for c in password):
        score += 1
    else:
        feedback.append("Add numbers")

    if any(c in string.punctuation for c in password):
        score += 1
    else:
        feedback.append("Add special characters (!@#$...)")

    common = ["password","123456","qwerty","abc123","letmein","admin","welcome"]
    if password.lower() in common:
        score = 0
        feedback.append("This is a commonly used password — change it!")

    if score <= 2:
        strength = "🔴 Weak"
    elif score <= 4:
        strength = "🟡 Fair"
    elif score <= 6:
        strength = "🟠 Good"
    else:
        strength = "🟢 Strong"

    return strength, score, feedback

def main():
    print("=== Password Strength Checker ===")
    while True:
        pwd = input("\nEnter password (or 'quit'): ")
        if pwd.lower() == "quit":
            break
        strength, score, feedback = check_strength(pwd)
        print(f"Strength: {strength} (score: {score}/7)")
        if feedback:
            print("Tips:")
            for tip in feedback:
                print(f"  • {tip}")

if __name__ == "__main__":
    main()
