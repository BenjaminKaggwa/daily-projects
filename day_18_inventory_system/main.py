import sqlite3

DB = "inventory.db"

def init():
    conn = sqlite3.connect(DB)
    conn.execute("""CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        category TEXT,
        price REAL NOT NULL,
        quantity INTEGER NOT NULL,
        updated TEXT DEFAULT (datetime('now'))
    )""")
    conn.commit()
    return conn

def add(conn, name, category, price, qty):
    conn.execute("INSERT INTO products (name, category, price, quantity) VALUES (?,?,?,?)",
                 (name, category, float(price), int(qty)))
    conn.commit()
    print(f"Added: {name} x{qty} @ RM{float(price):.2f}")

def view(conn):
    rows = conn.execute("SELECT * FROM products ORDER BY category, name").fetchall()
    if not rows: print("No products."); return
    print(f"\n{'ID':<5} {'Name':<22} {'Category':<14} {'Price':>9} {'Qty':>6} {'Value':>10}")
    print("-" * 70)
    total_val = 0
    for r in rows:
        val = r[4] * r[3]
        total_val += val
        print(f"{r[0]:<5} {r[1]:<22} {str(r[2]):<14} RM{r[3]:>7.2f} {r[4]:>6}  RM{val:>8.2f}")
    print(f"{'Total inventory value':>52}: RM{total_val:.2f}")

def update_qty(conn, pid, change):
    row = conn.execute("SELECT quantity, name FROM products WHERE id=?", (pid,)).fetchone()
    if not row: print("Product not found."); return
    new_qty = row[0] + change
    if new_qty < 0: print("Not enough stock."); return
    conn.execute("UPDATE products SET quantity=?, updated=datetime('now') WHERE id=?", (new_qty, pid))
    conn.commit()
    print(f"Updated {row[1]}: quantity now {new_qty}")

def low_stock(conn, threshold=5):
    rows = conn.execute("SELECT name, quantity FROM products WHERE quantity <= ?", (threshold,)).fetchall()
    if not rows: print("No low stock items.")
    else:
        print("\n⚠️  Low stock alert:")
        for r in rows:
            print(f"  {r[0]}: {r[1]} remaining")

def main():
    conn = init()
    print("=== Inventory System ===")
    while True:
        print("\n1.Add  2.View  3.Restock  4.Sell  5.Low Stock  6.Quit")
        c = input("Choice: ").strip()
        if c=="1": add(conn, input("Name: "), input("Category: "), input("Price (RM): "), input("Quantity: "))
        elif c=="2": view(conn)
        elif c=="3": view(conn); update_qty(conn, int(input("Product ID: ")), int(input("Add qty: ")))
        elif c=="4": view(conn); update_qty(conn, int(input("Product ID: ")), -int(input("Sell qty: ")))
        elif c=="5": low_stock(conn)
        elif c=="6": break

if __name__ == "__main__":
    main()
