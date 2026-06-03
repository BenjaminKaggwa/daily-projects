import sqlite3

DB = "contacts.db"

def init():
    conn = sqlite3.connect(DB)
    conn.execute("""CREATE TABLE IF NOT EXISTS contacts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        phone TEXT,
        email TEXT,
        notes TEXT
    )""")
    conn.commit()
    return conn

def add(conn, name, phone, email, notes):
    conn.execute("INSERT INTO contacts (name,phone,email,notes) VALUES (?,?,?,?)",
                 (name, phone, email, notes))
    conn.commit()
    print(f"Contact '{name}' added.")

def search(conn, query):
    rows = conn.execute("SELECT * FROM contacts WHERE name LIKE ? OR phone LIKE ? OR email LIKE ?",
                        (f"%{query}%",)*3).fetchall()
    display(rows)

def view_all(conn):
    rows = conn.execute("SELECT * FROM contacts ORDER BY name").fetchall()
    display(rows)

def display(rows):
    if not rows:
        print("No contacts found.")
        return
    print(f"\n{'ID':<5} {'Name':<20} {'Phone':<15} {'Email':<25} {'Notes'}")
    print("-" * 75)
    for r in rows:
        print(f"{r[0]:<5} {r[1]:<20} {str(r[2]):<15} {str(r[3]):<25} {r[4]}")

def delete(conn, cid):
    conn.execute("DELETE FROM contacts WHERE id=?", (cid,))
    conn.commit()
    print(f"Contact #{cid} deleted.")

def main():
    conn = init()
    print("=== Contact Book ===")
    while True:
        print("\n1. Add  2. View All  3. Search  4. Delete  5. Quit")
        c = input("Choice: ").strip()
        if c == "1":
            add(conn, input("Name: "), input("Phone: "), input("Email: "), input("Notes: "))
        elif c == "2":
            view_all(conn)
        elif c == "3":
            search(conn, input("Search: "))
        elif c == "4":
            view_all(conn)
            delete(conn, int(input("ID to delete: ")))
        elif c == "5":
            break

if __name__ == "__main__":
    main()
