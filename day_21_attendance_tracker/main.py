import sqlite3
from datetime import date

DB = "attendance.db"

def init():
    conn = sqlite3.connect(DB)
    conn.execute("""CREATE TABLE IF NOT EXISTS students (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL)""")
    conn.execute("""CREATE TABLE IF NOT EXISTS attendance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER, date TEXT, status TEXT,
        FOREIGN KEY(student_id) REFERENCES students(id)
    )""")
    conn.commit()
    return conn

def add_student(conn, name):
    conn.execute("INSERT INTO students (name) VALUES (?)", (name,))
    conn.commit()
    print(f"Student '{name}' added.")

def mark(conn):
    students = conn.execute("SELECT id, name FROM students").fetchall()
    if not students: print("No students."); return
    today = date.today().isoformat()
    print(f"\nMarking attendance for {today}")
    for sid, name in students:
        already = conn.execute("SELECT id FROM attendance WHERE student_id=? AND date=?", (sid, today)).fetchone()
        if already: print(f"  {name}: already marked"); continue
        s = input(f"  {name} — P(resent)/A(bsent)/L(ate): ").strip().upper()
        status = {"P":"Present","A":"Absent","L":"Late"}.get(s, "Absent")
        conn.execute("INSERT INTO attendance (student_id, date, status) VALUES (?,?,?)", (sid, today, status))
    conn.commit()
    print("Attendance saved.")

def report(conn):
    students = conn.execute("SELECT id, name FROM students").fetchall()
    print(f"\n{'Name':<20} {'Present':>8} {'Absent':>8} {'Late':>6} {'Rate':>8}")
    print("-" * 52)
    for sid, name in students:
        rows = conn.execute("SELECT status FROM attendance WHERE student_id=?", (sid,)).fetchall()
        total = len(rows)
        p = sum(1 for r in rows if r[0]=="Present")
        a = sum(1 for r in rows if r[0]=="Absent")
        l = sum(1 for r in rows if r[0]=="Late")
        rate = (p / total * 100) if total else 0
        print(f"{name:<20} {p:>8} {a:>8} {l:>6} {rate:>7.1f}%")

def main():
    conn = init()
    print("=== Attendance Tracker ===")
    while True:
        print("\n1.Add Student  2.Mark Today  3.Report  4.Quit")
        c = input("Choice: ").strip()
        if c=="1": add_student(conn, input("Name: "))
        elif c=="2": mark(conn)
        elif c=="3": report(conn)
        elif c=="4": break

if __name__ == "__main__":
    main()
