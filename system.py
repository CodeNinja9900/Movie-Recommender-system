import pandas as pd
import requests
import streamlit as st
import pickle
import os
import gzip

# Function to download file if not already downloaded
def download_if_needed(url, file_name):
    if not os.path.exists(file_name):
        print(f"Downloading {file_name}...")
        r = requests.get(url)
        with open(file_name, 'wb') as f:
            f.write(r.content)

# Download and load similarity.pkl.gz
download_if_needed(
    'https://drive.google.com/uc?export=download&id=1exw4llY2uw8Na6XIzp-eo0YYj_Ti7pfh',
    'similarity.pkl.gz'
)

with gzip.open('similarity.pkl.gz', 'rb') as f:
    similarity = pickle.load(f)

# Load the smaller file normally (must be in the repo or uploaded similarly)
movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

# Fetch movie poster
def fetch_postel(movie_id):
    response = requests.get(
        f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=fec312a4d375bf2a15e1bac80c05df2d'
    )
    data = response.json()
    return "https://image.tmdb.org/t/p/w500" + data['poster_path']

# Recommendation logic
def recommended(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distance = similarity[movie_index]
    movie_list = sorted(list(enumerate(distance)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movie = []
    recommended_movie_posters = []

    for i in movie_list:
        movie_id = movies.iloc[i[0]].id
        recommended_movie.append(movies.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_postel(movie_id))

    return recommended_movie, recommended_movie_posters

# Streamlit UI
st.title('🎬 Movie Recommender System')

selected_movie_name = st.selectbox(
    'Search for your favourite movies',
    movies['title'].values
)

if st.button('Recommend'):
    names, posters = recommended(selected_movie_name)

    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.markdown(f"**{names[i]}**")
            st.image(posters[i])
