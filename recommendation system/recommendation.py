import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

movies = pd.read_csv("movies.csv")

cv = CountVectorizer()

matrix = cv.fit_transform(movies["genre"])

similarity = cosine_similarity(matrix)

movie_name = input("Enter movie name: ").strip()

movie_found = movies[
    movies["title"].str.strip().str.lower()
    == movie_name.lower()
]

if movie_found.empty:
    print("Movie not found in database.")
else:
    movie_index = movie_found.index[0]

    scores = list(enumerate(similarity[movie_index]))

    scores = sorted(
        scores,
        key=lambda x: x[1],
        reverse=True
    )

    print("\nRecommended Movies:\n")

    for movie in scores[1:6]:
        print(movies.iloc[movie[0]].title)