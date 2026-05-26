import sqlite3

DB = "expenses.db"

def init():
    conn = sqlite3.connect(DB)
    conn.execute("""CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        description TEXT NOT NULL,
        amount REAL NOT NULL,
        category TEXT NOT NULL,
        date TEXT DEFAULT (date('now'))
    )""")
    conn.commit()
    return conn

def add(conn, description, amount, category):
    conn.execute("INSERT INTO expenses (description, amount, category) VALUES (?,?,?)",
                 (description, float(amount), category))
    conn.commit()
    print(f"Added: {description} — RM{float(amount):.2f} [{category}]")

def view(conn, category=None):
    if category:
        rows = conn.execute("SELECT id, description, amount, category, date FROM expenses WHERE category=?", (category,)).fetchall()
    else:
        rows = conn.execute("SELECT id, description, amount, category, date FROM expenses").fetchall()
    if not rows:
        print("No expenses found.")
        return
    print(f"\n{'ID':<5} {'Description':<20} {'Amount':>10} {'Category':<15} {'Date'}")
    print("-" * 60)
    for r in rows:
        print(f"{r[0]:<5} {r[1]:<20} RM{r[2]:>8.2f} {r[3]:<15} {r[4]}")
    total = sum(r[2] for r in rows)
    print(f"\nTotal: RM{total:.2f}")

def delete(conn, expense_id):
    conn.execute("DELETE FROM expenses WHERE id=?", (expense_id,))
    conn.commit()
    print(f"Deleted expense #{expense_id}")

def main():
    conn = init()
    print("=== Expense Tracker ===")
    while True:
        print("\n1. Add expense  2. View all  3. View by category  4. Delete  5. Quit")
        choice = input("Choice: ").strip()
        if choice == "1":
            desc = input("Description: ")
            amt  = input("Amount (RM): ")
            cat  = input("Category (food/transport/etc): ")
            add(conn, desc, amt, cat)
        elif choice == "2":
            view(conn)
        elif choice == "3":
            cat = input("Category: ")
            view(conn, cat)
        elif choice == "4":
            view(conn)
            eid = input("ID to delete: ")
            delete(conn, int(eid))
        elif choice == "5":
            print("Goodbye!")
            break

if __name__ == "__main__":
    main()
