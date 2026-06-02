import sys
import shutil
from pathlib import Path

CATEGORIES = {
    "Images":     [".jpg",".jpeg",".png",".gif",".bmp",".svg",".webp"],
    "Videos":     [".mp4",".mov",".avi",".mkv",".wmv"],
    "Documents":  [".pdf",".docx",".doc",".txt",".xlsx",".pptx",".csv"],
    "Audio":      [".mp3",".wav",".flac",".aac",".ogg"],
    "Code":       [".py",".js",".html",".css",".java",".cpp",".c",".ts",".json"],
    "Archives":   [".zip",".tar",".gz",".rar",".7z"],
    "Others":     []
}

def get_category(suffix):
    for cat, exts in CATEGORIES.items():
        if suffix.lower() in exts:
            return cat
    return "Others"

def organise(folder_path):
    folder = Path(folder_path)
    if not folder.exists():
        print(f"Folder not found: {folder_path}")
        return

    moved = 0
    for file in folder.iterdir():
        if file.is_file():
            cat     = get_category(file.suffix)
            dest    = folder / cat
            dest.mkdir(exist_ok=True)
            shutil.move(str(file), dest / file.name)
            print(f"Moved: {file.name} → {cat}/")
            moved += 1

    print(f"\nDone! Organised {moved} files.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py /path/to/folder")
    else:
        organise(sys.argv[1])
