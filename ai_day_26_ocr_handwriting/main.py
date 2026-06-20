import sys
from pathlib import Path
try:
    import pytesseract
    from PIL import Image, ImageEnhance, ImageFilter
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False

def preprocess(image_path):
    img = Image.open(image_path).convert("L")
    img = ImageEnhance.Contrast(img).enhance(2.0)
    img = img.filter(ImageFilter.SHARPEN)
    w, h = img.size
    if w < 1000:
        img = img.resize((w*2, h*2), Image.LANCZOS)
    return img

def extract_text(image_path, lang="eng"):
    img  = preprocess(image_path)
    config = "--oem 3 --psm 6"
    text = pytesseract.image_to_string(img, lang=lang, config=config)
    return text.strip()

def extract_data(image_path):
    img  = preprocess(image_path)
    data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
    words = [(data["text"][i], data["conf"][i]) for i in range(len(data["text"])) if data["text"][i].strip() and data["conf"][i] > 0]
    return words

def main():
    if not OCR_AVAILABLE:
        print("pytesseract or pillow not installed.")
        print("Run: pip install pytesseract pillow")
        print("Also install Tesseract from: https://github.com/UB-Mannheim/tesseract/wiki")
        return
    print("=== OCR Handwriting to Text ===")
    while True:
        print("\n1. Extract text from image  2. Extract with confidence  3. Quit")
        c = input("Choice: ").strip()
        if c == "1":
            path = input("Image path: ").strip()
            if not Path(path).exists(): print("File not found."); continue
            print("\nExtracting text...")
            text = extract_text(path)
            print(f"\n{'='*50}\n{text}\n{'='*50}")
            save = input("Save to file? (y/n): ").lower()
            if save == "y":
                out = Path(path).stem + "_text.txt"
                Path(out).write_text(text)
                print(f"Saved to {out}")
        elif c == "2":
            path = input("Image path: ").strip()
            if not Path(path).exists(): print("File not found."); continue
            words = extract_data(path)
            print(f"\n{'Word':<20} {'Confidence'}")
            print("-"*30)
            for word, conf in words:
                bar = "█" * int(conf/10)
                print(f"{word:<20} {conf}%  {bar}")
        elif c == "3":
            break

if __name__ == "__main__":
    main()
