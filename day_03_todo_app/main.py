import json
from pathlib import Path
from datetime import datetime

FILE = "todos.json"

def load():
    if Path(FILE).exists():
        with open(FILE) as f:
            return json.load(f)
    return []

def save(todos):
    with open(FILE, "w") as f:
        json.dump(todos, f, indent=2)

def show(todos):
    if not todos:
        print("No tasks yet!")
        return
    print(f"\n{'#':<5} {'Status':<10} {'Task':<30} {'Added'}")
    print("-" * 60)
    for i, t in enumerate(todos, 1):
        status = "✅ Done" if t["done"] else "⬜ Todo"
        print(f"{i:<5} {status:<10} {t['task']:<30} {t['date']}")

def main():
    todos = load()
    print("=== To-Do List ===")
    while True:
        print("\n1. Add  2. View  3. Complete  4. Delete  5. Quit")
        choice = input("Choice: ").strip()
        if choice == "1":
            task = input("Task: ").strip()
            todos.append({"task": task, "done": False, "date": datetime.now().strftime("%Y-%m-%d")})
            save(todos)
            print(f"Added: {task}")
        elif choice == "2":
            show(todos)
        elif choice == "3":
            show(todos)
            n = int(input("Mark task # as done: ")) - 1
            if 0 <= n < len(todos):
                todos[n]["done"] = True
                save(todos)
                print("Marked as done!")
        elif choice == "4":
            show(todos)
            n = int(input("Delete task #: ")) - 1
            if 0 <= n < len(todos):
                removed = todos.pop(n)
                save(todos)
                print(f"Deleted: {removed['task']}")
        elif choice == "5":
            print("Goodbye!")
            break

if __name__ == "__main__":
    main()
