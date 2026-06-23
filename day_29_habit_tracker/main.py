import sqlite3
from datetime import date, timedelta

DB = "habits.db"

def init():
    conn = sqlite3.connect(DB)
    conn.execute("CREATE TABLE IF NOT EXISTS habits (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL)")
    conn.execute("""CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        habit_id INTEGER, date TEXT,
        UNIQUE(habit_id, date),
        FOREIGN KEY(habit_id) REFERENCES habits(id)
    )""")
    conn.commit()
    return conn

def add_habit(conn, name):
    conn.execute("INSERT INTO habits (name) VALUES (?)", (name,))
    conn.commit()
    print(f"Habit '{name}' added.")

def log_today(conn):
    habits = conn.execute("SELECT id, name FROM habits").fetchall()
    if not habits: print("No habits yet."); return
    today = date.today().isoformat()
    print(f"\nLogging habits for {today}:")
    for hid, name in habits:
        done = conn.execute("SELECT id FROM logs WHERE habit_id=? AND date=?", (hid, today)).fetchone()
        if done: print(f"  ✅ {name} (already logged)"); continue
        c = input(f"  Did you complete '{name}'? (y/n): ").lower()
        if c == "y":
            conn.execute("INSERT OR IGNORE INTO logs (habit_id, date) VALUES (?,?)", (hid, today))
    conn.commit()
    print("Logged!")

def streak(conn, hid):
    today    = date.today()
    current  = 0
    check    = today
    while True:
        row = conn.execute("SELECT id FROM logs WHERE habit_id=? AND date=?",
                           (hid, check.isoformat())).fetchone()
        if row: current += 1; check -= timedelta(days=1)
        else: break
    return current

def report(conn):
    habits = conn.execute("SELECT id, name FROM habits").fetchall()
    if not habits: print("No habits."); return
    print(f"\n{'Habit':<25} {'Total':>7} {'Streak':>8} {'Last 7 days'}")
    print("-" * 55)
    today = date.today()
    for hid, name in habits:
        total = conn.execute("SELECT COUNT(*) FROM logs WHERE habit_id=?", (hid,)).fetchone()[0]
        s     = streak(conn, hid)
        week  = ""
        for i in range(6,-1,-1):
            d   = (today - timedelta(days=i)).isoformat()
            row = conn.execute("SELECT id FROM logs WHERE habit_id=? AND date=?", (hid, d)).fetchone()
            week += "🟩" if row else "⬜"
        print(f"{name:<25} {total:>7} {s:>6}🔥  {week}")

def main():
    conn = init()
    print("=== Habit Tracker ===")
    while True:
        print("\n1.Add Habit  2.Log Today  3.Report  4.Quit")
        c = input("Choice: ").strip()
        if c=="1": add_habit(conn, input("Habit name: "))
        elif c=="2": log_today(conn)
        elif c=="3": report(conn)
        elif c=="4": break

if __name__ == "__main__":
    main()
