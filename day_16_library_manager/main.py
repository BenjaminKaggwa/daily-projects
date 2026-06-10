import sqlite3

DB = "library.db"

def init():
    conn = sqlite3.connect(DB)
    conn.execute("""CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        isbn TEXT,
        available INTEGER DEFAULT 1
    )""")
    conn.commit()
    return conn

def add(conn, title, author, isbn):
    conn.execute("INSERT INTO books (title, author, isbn) VALUES (?,?,?)", (title, author, isbn))
    conn.commit()
    print(f"Added: '{title}' by {author}")

def view(conn, available_only=False):
    q = "SELECT * FROM books WHERE available=1" if available_only else "SELECT * FROM books"
    rows = conn.execute(q).fetchall()
    if not rows: print("No books."); return
    print(f"\n{'ID':<5} {'Title':<30} {'Author':<20} {'ISBN':<15} {'Status'}")
    print("-" * 80)
    for r in rows:
        status = "✅ Available" if r[4] else "❌ Borrowed"
        print(f"{r[0]:<5} {r[1]:<30} {r[2]:<20} {str(r[3]):<15} {status}")

def borrow(conn, book_id):
    row = conn.execute("SELECT available FROM books WHERE id=?", (book_id,)).fetchone()
    if not row: print("Book not found.")
    elif not row[0]: print("Book already borrowed.")
    else:
        conn.execute("UPDATE books SET available=0 WHERE id=?", (book_id,))
        conn.commit(); print(f"Book #{book_id} borrowed.")

def returnbook(conn, book_id):
    conn.execute("UPDATE books SET available=1 WHERE id=?", (book_id,))
    conn.commit(); print(f"Book #{book_id} returned.")

def search(conn, query):
    rows = conn.execute("SELECT * FROM books WHERE title LIKE ? OR author LIKE ?",
                        (f"%{query}%",)*2).fetchall()
    if not rows: print("No results.")
    else:
        for r in rows:
            status = "Available" if r[4] else "Borrowed"
            print(f"  [{r[0]}] {r[1]} by {r[2]} — {status}")

def main():
    conn = init()
    print("=== Library Manager ===")
    while True:
        print("\n1.Add  2.View All  3.Available  4.Borrow  5.Return  6.Search  7.Quit")
        c = input("Choice: ").strip()
        if c=="1": add(conn, input("Title: "), input("Author: "), input("ISBN: "))
        elif c=="2": view(conn)
        elif c=="3": view(conn, available_only=True)
        elif c=="4": view(conn); borrow(conn, int(input("Book ID: ")))
        elif c=="5": returnbook(conn, int(input("Book ID: ")))
        elif c=="6": search(conn, input("Search: "))
        elif c=="7": break

if __name__ == "__main__":
    main()
