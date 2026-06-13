import os
from pathlib import Path
from datetime import datetime

NOTES_DIR = Path("notes")
NOTES_DIR.mkdir(exist_ok=True)

def create(title):
    slug     = title.lower().replace(" ", "_").replace("/","")
    filename = NOTES_DIR / f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{slug}.md"
    print(f"\nType your note (type END on a new line to finish):")
    lines = [f"# {title}", f"*Created: {datetime.now().strftime('%Y-%m-%d %H:%M')}*", ""]
    while True:
        line = input()
        if line.strip() == "END":
            break
        lines.append(line)
    filename.write_text("\n".join(lines))
    print(f"\nNote saved: {filename.name}")

def list_notes():
    notes = sorted(NOTES_DIR.glob("*.md"))
    if not notes: print("No notes yet."); return notes
    print(f"\n{'#':<5} {'Filename':<45} {'Size'}")
    print("-" * 60)
    for i, n in enumerate(notes, 1):
        print(f"{i:<5} {n.name:<45} {n.stat().st_size} bytes")
    return notes

def view(notes, n):
    if 1 <= n <= len(notes):
        print(f"\n{'='*50}")
        print(notes[n-1].read_text())
        print("="*50)

def delete(notes, n):
    if 1 <= n <= len(notes):
        notes[n-1].unlink()
        print(f"Deleted: {notes[n-1].name}")

def search(query):
    results = []
    for f in NOTES_DIR.glob("*.md"):
        content = f.read_text().lower()
        if query.lower() in content:
            results.append(f)
    if not results: print("No matching notes.")
    else:
        print(f"\nFound {len(results)} note(s):")
        for r in results:
            print(f"  {r.name}")

def main():
    print("=== Markdown Notes ===")
    while True:
        print("\n1.New  2.List  3.View  4.Delete  5.Search  6.Quit")
        c = input("Choice: ").strip()
        if c=="1": create(input("Note title: "))
        elif c=="2": list_notes()
        elif c=="3":
            notes = list_notes()
            if notes: view(notes, int(input("View note #: ")))
        elif c=="4":
            notes = list_notes()
            if notes: delete(notes, int(input("Delete note #: ")))
        elif c=="5": search(input("Search for: "))
        elif c=="6": break

if __name__ == "__main__":
    main()
