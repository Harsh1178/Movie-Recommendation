from flask import Flask, render_template, request
import pandas as pd
import requests
import random

app = Flask(__name__)

df = pd.read_csv('new-data.csv')
df.columns = df.columns.str.strip()

titles = df['title'].dropna().tolist()

def recomend(movie):
    match = df[df['title'] == movie]

    if match.empty:
        return []

    idx = match.index[0]

    k = df.iloc[idx]['similar-movie']
    k = k.replace('[', "").replace("]", "")
    kk = k.split(',')

    results = []

    for i in kk:
        i = int(i.strip())
        movie_id = df.iloc[i].id

        # 🔥 TMDB API
        url = f"https://api.themoviedb.org/3/movie/{movie_id}/images"

        headers = {
            "accept": "application/json",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJhZjc3YzZkNmUwMWNjNjNkNzIwNDZmYTYxN2M2OWU4ZSIsIm5iZiI6MTc2MjI4MDI0OS40ODYsInN1YiI6IjY5MGE0MzM5OWU3YzI2YWM5NjYxYzliMSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.XqNm9e34orlo-BmZE08j6cYyJEwhHkJ6dm75-twfskc"
        }

        response = requests.get(url, headers=headers)
        data = response.json()

        # Handle missing poster
        if data.get('posters'):
            poster_path = data['posters'][0]['file_path']
            poster = 'https://image.tmdb.org/t/p/w500/' + poster_path
        else:
            poster = "https://via.placeholder.com/300x450?text=No+Image"

        title = df.iloc[i]['title']

        results.append((title, poster))

    return results


@app.route('/', methods=['GET', 'POST'])
def index():
    movies = []

    if request.method == 'POST':
        movie = request.form.get('movie')

        if movie:
            movies = recomend(movie)

    else:
        # 🔥 RANDOM DEFAULT MOVIE
        if len(titles) > 0:
            random_movie = random.choice(titles)
            movies = recomend(random_movie)

    return render_template(
        'index.html',
        titles=sorted(titles),
        movies=movies
    )

if __name__ == '__main__':
    app.run(debug=True)