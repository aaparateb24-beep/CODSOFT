import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load dataset
movies = pd.read_csv("movies.csv")

# Build similarity matrix
cv = CountVectorizer()
matrix = cv.fit_transform(movies["genre"])
similarity = cosine_similarity(matrix)

print("=" * 50)
print("🎬 MOVIE RECOMMENDATION SYSTEM")
print("=" * 50)

print("\nAvailable Movies:\n")

for movie in movies["title"]:
    print(f"• {movie}")

print("\n" + "=" * 50)

movie_name = input("Enter a movie name: ").strip().lower()

movie_found = movies[
    movies["title"].str.strip().str.lower() == movie_name
]

if movie_found.empty:
    print("\n❌ Movie not found!")
    print("Please enter one of the available movie names.")
else:
    movie_index = movie_found.index[0]

    scores = list(enumerate(similarity[movie_index]))

    scores = sorted(
        scores,
        key=lambda x: x[1],
        reverse=True
    )

    print("\n" + "=" * 50)
    print("🎯 Recommended Movies")
    print("=" * 50)

    for i, movie in enumerate(scores[1:6], start=1):
        print(f"{i}. {movies.iloc[movie[0]].title}")

    print("\nThank you for using the Movie Recommendation System!")