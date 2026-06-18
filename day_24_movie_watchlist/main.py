import sqlite3

DB = "movies.db"

def init():
    conn = sqlite3.connect(DB)
    conn.execute("""CREATE TABLE IF NOT EXISTS movies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL, genre TEXT, year INTEGER,
        rating REAL, watched INTEGER DEFAULT 0, notes TEXT
    )""")
    conn.commit()
    return conn

def add(conn, title, genre, year):
    conn.execute("INSERT INTO movies (title, genre, year) VALUES (?,?,?)", (title, genre, year))
    conn.commit()
    print(f"Added: {title}")

def view(conn, watched=None, genre=None):
    q = "SELECT * FROM movies WHERE 1=1"
    params = []
    if watched is not None: q += " AND watched=?"; params.append(watched)
    if genre: q += " AND genre LIKE ?"; params.append(f"%{genre}%")
    rows = conn.execute(q, params).fetchall()
    if not rows: print("No movies found."); return
    print(f"\n{'ID':<5} {'Title':<28} {'Genre':<14} {'Year':<6} {'Rating':<8} {'Seen'}")
    print("-" * 68)
    for r in rows:
        seen   = "✅" if r[5] else "⬜"
        rating = f"{r[4]:.1f}/10" if r[4] else "—"
        print(f"{r[0]:<5} {r[1]:<28} {str(r[2]):<14} {str(r[3]):<6} {rating:<8} {seen}")

def mark_watched(conn, mid, rating):
    conn.execute("UPDATE movies SET watched=1, rating=? WHERE id=?", (rating, mid))
    conn.commit()
    print(f"Marked as watched with rating {rating}/10")

def main():
    conn = init()
    print("=== Movie Watchlist ===")
    while True:
        print("\n1.Add  2.All  3.Watchlist  4.Watched  5.By Genre  6.Mark Watched  7.Quit")
        c = input("Choice: ").strip()
        if c=="1": add(conn, input("Title: "), input("Genre: "), input("Year: "))
        elif c=="2": view(conn)
        elif c=="3": view(conn, watched=0)
        elif c=="4": view(conn, watched=1)
        elif c=="5": view(conn, genre=input("Genre: "))
        elif c=="6":
            view(conn, watched=0)
            mid    = int(input("Movie ID: "))
            rating = float(input("Rating (1-10): "))
            mark_watched(conn, mid, rating)
        elif c=="7": break

if __name__ == "__main__":
    main()
