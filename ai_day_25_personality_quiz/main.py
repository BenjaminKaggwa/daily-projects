QUESTIONS = [
    {
        "q": "At a party, you usually:",
        "options": ["A) Talk to many new people enthusiastically",
                    "B) Stick to a small group you know well",
                    "C) Find a quiet corner and observe",
                    "D) Leave early — parties drain you"],
        "scores": {"E": [3,1,0,0], "I": [0,1,2,3]}
    },
    {
        "q": "When solving a problem, you prefer:",
        "options": ["A) Logical step-by-step analysis",
                    "B) Intuition and gut feeling",
                    "C) Discussing with others first",
                    "D) Trying random things until it works"],
        "scores": {"T": [3,0,1,1], "F": [0,2,3,1]}
    },
    {
        "q": "Your workspace is usually:",
        "options": ["A) Highly organised with clear systems",
                    "B) A bit cluttered but you know where things are",
                    "C) Creative chaos — organised in your mind",
                    "D) It changes depending on your mood"],
        "scores": {"J": [3,2,0,1], "P": [0,1,3,2]}
    },
    {
        "q": "When learning something new, you prefer:",
        "options": ["A) Concrete examples and hands-on practice",
                    "B) Big picture concepts and theories",
                    "C) Reading detailed documentation",
                    "D) Watching someone else do it first"],
        "scores": {"S": [3,0,2,2], "N": [0,3,1,1]}
    },
    {
        "q": "Under stress, you tend to:",
        "options": ["A) Make a detailed action plan",
                    "B) Talk it through with someone",
                    "C) Go quiet and process alone",
                    "D) Distract yourself with other things"],
        "scores": {"T": [3,0,2,1], "F": [0,3,1,1]}
    },
]

PROFILES = {
    "ENTJ": ("The Commander",    "Natural leader. Strategic thinker. Drives results and inspires teams."),
    "INTJ": ("The Architect",    "Independent visionary. Loves systems and long-term planning."),
    "ENFP": ("The Campaigner",   "Creative, enthusiastic, and people-focused. Full of ideas."),
    "INFP": ("The Mediator",     "Empathetic idealist. Values authenticity and deeper meaning."),
    "ESTJ": ("The Executive",    "Organised, practical, and dependable. Gets things done."),
    "ISTJ": ("The Inspector",    "Reliable, detail-oriented, and thorough. Follows through always."),
    "ENTP": ("The Debater",      "Quick thinker. Loves challenging ideas and finding new angles."),
    "INTP": ("The Logician",     "Analytical, logical, and loves deep intellectual problems."),
    "ENFJ": ("The Protagonist",  "Charismatic leader who inspires and supports those around them."),
    "INFJ": ("The Advocate",     "Insightful, principled, and deeply committed to their values."),
    "ESFP": ("The Entertainer",  "Spontaneous, energetic, and loves bringing joy to others."),
    "ISFP": ("The Adventurer",   "Flexible artist who lives in the present and follows their heart."),
    "ESTP": ("The Entrepreneur", "Bold, practical, and thrives on immediate action and results."),
    "ISTP": ("The Virtuoso",     "Calm problem-solver who loves understanding how things work."),
    "ESFJ": ("The Consul",       "Caring, social, and loves supporting the people around them."),
    "ISFJ": ("The Defender",     "Warm, dedicated, and always ready to protect and help others."),
}

def analyse(answers):
    E, I, T, F, S, N, J, P = 0, 0, 0, 0, 0, 0, 0, 0
    for i, ans in enumerate(answers):
        q = QUESTIONS[i]
        idx = ord(ans.upper()) - ord("A")
        if "E" in q["scores"]: E += q["scores"]["E"][idx]
        if "I" in q["scores"]: I += q["scores"]["I"][idx]
        if "T" in q["scores"]: T += q["scores"]["T"][idx]
        if "F" in q["scores"]: F += q["scores"]["F"][idx]
        if "S" in q["scores"]: S += q["scores"]["S"][idx]
        if "N" in q["scores"]: N += q["scores"]["N"][idx]
        if "J" in q["scores"]: J += q["scores"]["J"][idx]
        if "P" in q["scores"]: P += q["scores"]["P"][idx]
    mbti = ("E" if E >= I else "I") + ("S" if S >= N else "N") + ("T" if T >= F else "F") + ("J" if J >= P else "P")
    return mbti, {"E":E,"I":I,"T":T,"F":F,"S":S,"N":N,"J":J,"P":P}

def main():
    print("=== AI Personality Quiz ===")
    print("Answer 5 questions to discover your personality type.\n")
    while True:
        print("1. Take quiz  2. Quit")
        c = input("Choice: ").strip()
        if c == "1":
            name = input("Your name: ").strip()
            answers = []
            for i, q in enumerate(QUESTIONS, 1):
                print(f"\nQ{i}: {q['q']}")
                for opt in q["options"]:
                    print(f"  {opt}")
                while True:
                    ans = input("Your answer (A/B/C/D): ").strip().upper()
                    if ans in "ABCD" and len(ans) == 1:
                        answers.append(ans); break
                    print("Please enter A, B, C, or D")
            mbti, scores = analyse(answers)
            name_str, desc = PROFILES.get(mbti, ("Unknown", "Unique personality!"))
            print(f"\n{'='*55}")
            print(f"  {name}'s Personality Profile")
            print(f"{'='*55}")
            print(f"  Type        : {mbti} — {name_str}")
            print(f"  Description : {desc}")
            print(f"\n  Trait breakdown:")
            pairs = [("Extraversion","Introversion","E","I"),("Sensing","Intuition","S","N"),
                     ("Thinking","Feeling","T","F"),("Judging","Perceiving","J","P")]
            for t1, t2, k1, k2 in pairs:
                s1, s2 = scores[k1], scores[k2]
                total  = s1 + s2 if s1 + s2 > 0 else 1
                pct    = s1 / total * 100
                bar    = "█" * int(pct/5)
                print(f"  {t1:<14} {bar:<20} {pct:.0f}% {k1} | {k2} {100-pct:.0f}%")
            print("="*55)
        elif c == "2":
            break

if __name__ == "__main__":
    main()
