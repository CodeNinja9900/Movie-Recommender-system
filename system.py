import pandas as pd
import requests
import  streamlit as st
import pickle

def fetch_poster(movie_id):
    try:
        response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=fec312a4d375bf2a15e1bac80c05df2d'.format(movie_id))
        data = response.json()
        if 'poster_path' in data and data['poster_path']:
            return "https://image.tmdb.org/t/p/w500" + data['poster_path']
        return "https://via.placeholder.com/500x750?text=No+Poster"
    except Exception as e:
        print(f"Error fetching poster: {e}")
        return "https://via.placeholder.com/500x750?text=Error+Loading+Poster"



def recommended(movie):
    movie_index = movies[movies ['title'] == movie].index[0]
    distance = similarity[movie_index]
    movie_list = sorted(list(enumerate(distance)), reverse=True, key=lambda x:x[1])[1:6]

    recommended_movie = []
    recommended_movie_posters = []
    for i in movie_list:
        movie_id = movies.iloc[i[0]].id
        recommended_movie.append(movies.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_poster(movie_id))
        print(movies.iloc[i[0]].title)
    return  recommended_movie, recommended_movie_posters



import os

# Show loading message
st.sidebar.write("Loading movie data...")

# Load movies data
try:
    movies_dict = pickle.load(open('movies_dict.pkl','rb'))
    movies = pd.DataFrame(movies_dict)
except FileNotFoundError:
    st.error("movies_dict.pkl not found. Please ensure the file is in the same directory as the script.")
    st.stop()

# Show loading message for similarity matrix
st.sidebar.write("Loading similarity matrix...")

# Try to load similarity matrix
similarity = None
similarity_path = os.path.join(os.path.dirname(__file__), 'similarity.pkl.gz')

try:
    import gzip
    with gzip.open(similarity_path, 'rb') as f:
        similarity = pickle.load(f)
    st.sidebar.success("✅ Data loaded successfully!")
except FileNotFoundError:
    st.error(f"Similarity matrix file not found at: {similarity_path}")
    st.error("Please ensure the similarity.pkl.gz file is present in the application directory.")
    st.stop()
except gzip.BadGzipFile:
    st.error("The similarity matrix file is corrupted. Please provide a valid compressed file.")
    st.stop()
except Exception as e:
    st.error(f"Error loading similarity matrix: {str(e)}")
    st.stop()

st.title('movie recommender system')

selected_movie_name = st.selectbox(
 'Search for your favourite movies',
    movies['title'].values
)

if st.button('Recommend'):
    try:
        names, posters = recommended(selected_movie_name)
        if not names:
            st.error("No recommendations found for this movie.")
        else:
            # Create only as many columns as we have recommendations
            num_recommendations = len(names)
            cols = st.columns(min(5, num_recommendations))

            # Populate each column dynamically
            for idx, col in enumerate(cols):
                if idx < len(names):
                    with col:
                        st.markdown(names[idx])
                        st.image(posters[idx])
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

