import sqlite3
import hashlib
import os

DB = "users.db"

def init():
    conn = sqlite3.connect(DB)
    conn.execute("""CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        salt TEXT NOT NULL,
        created TEXT DEFAULT (datetime('now'))
    )""")
    conn.commit()
    return conn

def hash_password(password, salt=None):
    if not salt:
        salt = os.urandom(16).hex()
    h = hashlib.sha256((salt + password).encode()).hexdigest()
    return h, salt

def register(conn, username, password):
    h, salt = hash_password(password)
    try:
        conn.execute("INSERT INTO users (username, password_hash, salt) VALUES (?,?,?)", (username, h, salt))
        conn.commit()
        print(f"✅ Account created for '{username}'")
    except sqlite3.IntegrityError:
        print("❌ Username already taken.")

def login(conn, username, password):
    row = conn.execute("SELECT password_hash, salt FROM users WHERE username=?", (username,)).fetchone()
    if not row:
        print("❌ User not found.")
        return False
    h, _ = hash_password(password, row[1])
    if h == row[0]:
        print(f"✅ Welcome back, {username}!")
        return True
    print("❌ Incorrect password.")
    return False

def main():
    conn = init()
    print("=== Login System ===")
    while True:
        print("\n1. Register  2. Login  3. Quit")
        c = input("Choice: ").strip()
        if c == "1":
            u = input("Username: ")
            p = input("Password: ")
            register(conn, u, p)
        elif c == "2":
            u = input("Username: ")
            p = input("Password: ")
            login(conn, u, p)
        elif c == "3":
            break

if __name__ == "__main__":
    main()
