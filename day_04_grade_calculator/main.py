import sqlite3

DB = "grades.db"

def init():
    conn = sqlite3.connect(DB)
    conn.execute("""CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        subject TEXT NOT NULL,
        marks REAL NOT NULL,
        grade TEXT,
        gpa REAL
    )""")
    conn.commit()
    return conn

def calculate(marks):
    if marks >= 90: return "A+", 4.0
    if marks >= 80: return "A",  4.0
    if marks >= 75: return "A-", 3.7
    if marks >= 70: return "B+", 3.3
    if marks >= 65: return "B",  3.0
    if marks >= 60: return "B-", 2.7
    if marks >= 55: return "C+", 2.3
    if marks >= 50: return "C",  2.0
    if marks >= 45: return "D",  1.0
    return "F", 0.0

def add(conn, name, subject, marks):
    grade, gpa = calculate(float(marks))
    conn.execute("INSERT INTO students (name, subject, marks, grade, gpa) VALUES (?,?,?,?,?)",
                 (name, subject, float(marks), grade, gpa))
    conn.commit()
    status = "PASS" if float(marks) >= 50 else "FAIL"
    print(f"\n{name} | {subject} | {marks} marks | Grade: {grade} | GPA: {gpa} | {status}")

def view(conn):
    rows = conn.execute("SELECT name, subject, marks, grade, gpa FROM students").fetchall()
    if not rows:
        print("No records yet.")
        return
    print(f"\n{'Name':<20} {'Subject':<20} {'Marks':>7} {'Grade':<8} {'GPA'}")
    print("-" * 60)
    for r in rows:
        print(f"{r[0]:<20} {r[1]:<20} {r[2]:>7.1f} {r[3]:<8} {r[4]:.2f}")

def main():
    conn = init()
    print("=== Student Grade Calculator ===")
    while True:
        print("\n1. Add result  2. View all  3. Quit")
        choice = input("Choice: ").strip()
        if choice == "1":
            name    = input("Student name: ")
            subject = input("Subject: ")
            marks   = input("Marks (0-100): ")
            add(conn, name, subject, marks)
        elif choice == "2":
            view(conn)
        elif choice == "3":
            break

if __name__ == "__main__":
    main()
