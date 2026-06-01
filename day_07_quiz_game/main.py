import sqlite3
import random

DB = "quiz.db"

QUESTIONS = [
    ("What does CPU stand for?", ["Central Processing Unit","Computer Personal Unit","Control Processing Utility","Central Program Unit"], "Central Processing Unit"),
    ("Which language is known as the 'language of the web'?", ["Python","JavaScript","Java","C++"], "JavaScript"),
    ("What does SQL stand for?", ["Structured Query Language","Simple Query Logic","Standard Query Language","Structured Question Logic"], "Structured Query Language"),
    ("What is the binary value of decimal 10?", ["1010","1100","1001","1110"], "1010"),
    ("Which data structure uses LIFO?", ["Queue","Stack","Linked List","Tree"], "Stack"),
    ("What is the time complexity of binary search?", ["O(n)","O(n²)","O(log n)","O(1)"], "O(log n)"),
    ("Which of these is NOT a programming language?", ["Python","HTML","Java","Rust"], "HTML"),
    ("What does RAM stand for?", ["Random Access Memory","Read Access Module","Run Application Memory","Random Application Module"], "Random Access Memory"),
    ("What symbol is used for comments in Python?", ["//","#","/*","--"], "#"),
    ("Which protocol is used to load websites?", ["FTP","SSH","HTTP","SMTP"], "HTTP"),
]

def init():
    conn = sqlite3.connect(DB)
    conn.execute("""CREATE TABLE IF NOT EXISTS scores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT, score INTEGER, total INTEGER, date TEXT DEFAULT (date('now'))
    )""")
    conn.commit()
    return conn

def play(conn):
    name  = input("Enter your name: ")
    qs    = random.sample(QUESTIONS, 5)
    score = 0
    for i, (q, opts, ans) in enumerate(qs, 1):
        print(f"\nQ{i}: {q}")
        random.shuffle(opts)
        for j, o in enumerate(opts, 1):
            print(f"  {j}. {o}")
        choice = input("Your answer (1-4): ").strip()
        try:
            chosen = opts[int(choice) - 1]
            if chosen == ans:
                print("✅ Correct!")
                score += 1
            else:
                print(f"❌ Wrong! Answer: {ans}")
        except:
            print(f"❌ Invalid. Answer: {ans}")
    print(f"\n🎉 {name} scored {score}/5!")
    conn.execute("INSERT INTO scores (name, score, total) VALUES (?,?,?)", (name, score, 5))
    conn.commit()

def leaderboard(conn):
    rows = conn.execute("SELECT name, score, total, date FROM scores ORDER BY score DESC LIMIT 10").fetchall()
    print(f"\n{'Name':<20} {'Score':<10} {'Date'}")
    print("-" * 40)
    for r in rows:
        print(f"{r[0]:<20} {r[1]}/{r[2]:<8} {r[3]}")

def main():
    conn = init()
    print("=== Quiz Game ===")
    while True:
        print("\n1. Play  2. Leaderboard  3. Quit")
        c = input("Choice: ").strip()
        if c == "1": play(conn)
        elif c == "2": leaderboard(conn)
        elif c == "3": break

if __name__ == "__main__":
    main()
