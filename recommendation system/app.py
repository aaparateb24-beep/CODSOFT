import customtkinter as ctk
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# -----------------------
# Theme
# -----------------------

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")
# -----------------------
# Load Dataset
# -----------------------

movies = pd.read_csv("movies.csv")

cv = CountVectorizer()

matrix = cv.fit_transform(movies["genre"])

similarity = cosine_similarity(matrix)
def recommend():

    movie_name = movie_dropdown.get()

    result_box.delete("1.0", "end")

    if movie_name == "Select a Movie":
        result_box.insert("end", "❌ Please select a movie.")
        return

    movie_found = movies[
        movies["title"].str.strip().str.lower()
        == movie_name.strip().lower()
    ]

    if movie_found.empty:
        result_box.insert("end", "❌ Movie not found.")
        return

    movie_index = movie_found.index[0]

    scores = list(enumerate(similarity[movie_index]))

    scores = sorted(
        scores,
        key=lambda x: x[1],
        reverse=True
    )

    result_box.insert("end", "🎯 Top 5 Recommendations\n\n")

    for movie in scores[1:6]:
        result_box.insert(
            "end",
            f"⭐ {movies.iloc[movie[0]].title}\n"
        )
# -----------------------
# Main Window
# -----------------------

app = ctk.CTk()

app.geometry("900x650")

app.title("Movie Recommendation System")

app.resizable(False, False)
title = ctk.CTkLabel(
    app,
    text="🎬 Movie Recommendation System",
    font=("Arial",30,"bold")
)

title.pack(pady=20)

subtitle = ctk.CTkLabel(
    app,
    text="CODSOFT Internship Project",
    font=("Arial",16)
)

subtitle.pack()
movie_dropdown = ctk.CTkComboBox(
    app,
    values=list(movies["title"]),
    width=420,
    height=40,
    font=("Arial",15)
)

movie_dropdown.pack(pady=35)

movie_dropdown.set("Select a Movie")
recommend_btn = ctk.CTkButton(
    app,
    text="🎥 Recommend Movies",
    width=220,
    height=45,
    command=recommend
)

recommend_btn.pack()
result_box = ctk.CTkTextbox(
    app,
    width=700,
    height=250,
    font=("Arial",16)
)

result_box.pack(pady=30)
result_box.insert(
    "end",
    "👋 Welcome!\n\nSelect a movie and click 'Recommend Movies'."
)
footer = ctk.CTkLabel(
    app,
    text="Developed by Aarya",
    font=("Arial",12)
)

footer.pack(side="bottom", pady=15)
app.mainloop()