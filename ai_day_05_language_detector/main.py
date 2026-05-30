from langdetect import detect, detect_langs
from langdetect.lang_detect_exception import LangDetectException

LANGUAGE_NAMES = {
    "en":"English","ms":"Malay","zh-cn":"Chinese (Simplified)","zh-tw":"Chinese (Traditional)",
    "ar":"Arabic","fr":"French","de":"German","es":"Spanish","it":"Italian","pt":"Portuguese",
    "ru":"Russian","ja":"Japanese","ko":"Korean","hi":"Hindi","th":"Thai","vi":"Vietnamese",
    "id":"Indonesian","nl":"Dutch","sv":"Swedish","pl":"Polish","tr":"Turkish","uk":"Ukrainian",
    "cs":"Czech","ro":"Romanian","hu":"Hungarian","da":"Danish","fi":"Finnish","no":"Norwegian",
}

def get_name(code):
    return LANGUAGE_NAMES.get(code, code.upper())

def analyse(text):
    try:
        top    = detect(text)
        all_langs = detect_langs(text)
        return top, all_langs
    except LangDetectException:
        return None, []

def main():
    print("=== Language Detector ===")
    print("Supports 55+ languages\n")
    samples = [
        "Hello, how are you today?",
        "Bonjour, comment allez-vous?",
        "Hola, ¿cómo estás?",
        "Apa khabar? Saya baik-baik saja.",
        "你好，今天怎么样？",
        "こんにちは、お元気ですか？",
    ]
    print("Sample detections:")
    for s in samples:
        lang, _ = analyse(s)
        print(f"  '{s[:40]}' → {get_name(lang)}")
    print()
    while True:
        text = input("Enter text to detect (or 'quit'): ").strip()
        if text.lower() == "quit":
            break
        if len(text) < 3:
            print("Please enter at least 3 characters."); continue
        top, all_langs = analyse(text)
        if not top:
            print("Could not detect language."); continue
        print(f"\n  Primary language : {get_name(top)} ({top})")
        print(f"  Probabilities    :")
        for l in all_langs[:3]:
            print(f"    {get_name(str(l.lang)):<30} {l.prob*100:.1f}%")
        print()

if __name__ == "__main__":
    main()
