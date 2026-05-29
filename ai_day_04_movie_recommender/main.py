import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

MOVIES = [
    {"title": "The Dark Knight",          "genres": "action crime drama thriller superhero"},
    {"title": "Inception",                "genres": "action sci-fi thriller mystery dream"},
    {"title": "Interstellar",             "genres": "sci-fi drama adventure space time"},
    {"title": "The Matrix",               "genres": "action sci-fi thriller dystopia"},
    {"title": "Pulp Fiction",             "genres": "crime drama thriller dark comedy"},
    {"title": "The Godfather",            "genres": "crime drama thriller mafia"},
    {"title": "Forrest Gump",             "genres": "drama romance comedy history"},
    {"title": "The Shawshank Redemption", "genres": "drama crime hope prison"},
    {"title": "Avengers Endgame",         "genres": "action superhero sci-fi adventure"},
    {"title": "Parasite",                 "genres": "thriller drama dark comedy social"},
    {"title": "Get Out",                  "genres": "horror thriller mystery social"},
    {"title": "Knives Out",               "genres": "mystery comedy thriller crime"},
    {"title": "La La Land",               "genres": "romance drama musical comedy"},
    {"title": "Whiplash",                 "genres": "drama music passion obsession"},
    {"title": "The Social Network",       "genres": "drama biography tech ambition"},
    {"title": "Mad Max Fury Road",        "genres": "action adventure post-apocalyptic"},
    {"title": "Her",                      "genres": "sci-fi romance drama AI future"},
    {"title": "Ex Machina",               "genres": "sci-fi thriller AI drama mystery"},
    {"title": "Arrival",                  "genres": "sci-fi drama mystery time language"},
    {"title": "Dune",                     "genres": "sci-fi adventure drama epic space"},
]

df      = pd.DataFrame(MOVIES)
tfidf   = TfidfVectorizer()
tfidf_matrix = tfidf.fit_transform(df["genres"])
sim_matrix   = cosine_similarity(tfidf_matrix)

def recommend(title, n=5):
    title = title.strip().lower()
    matches = df[df["title"].str.lower() == title]
    if matches.empty:
        partial = df[df["title"].str.lower().str.contains(title)]
        if partial.empty:
            return None, []
        matches = partial
    idx     = matches.index[0]
    scores  = list(enumerate(sim_matrix[idx]))
    scores  = sorted(scores, key=lambda x: x[1], reverse=True)
    results = [(df.iloc[i]["title"], round(s*100,1)) for i, s in scores if i != idx][:n]
    return df.iloc[idx]["title"], results

def main():
    print("=== Movie Recommendation Engine ===")
    print("\nAvailable movies:")
    for m in df["title"]:
        print(f"  • {m}")
    while True:
        print("\n1. Get recommendations  2. Quit")
        c = input("Choice: ").strip()
        if c == "1":
            title  = input("Movie title: ")
            found, recs = recommend(title)
            if not found:
                print("Movie not found. Try another title.")
                continue
            print(f"\nBecause you liked '{found}', you might enjoy:\n")
            for i, (t, score) in enumerate(recs, 1):
                bar = "█" * int(score / 10)
                print(f"  {i}. {t:<35} {score:.0f}% match  {bar}")
        elif c == "2":
            break

if __name__ == "__main__":
    main()
