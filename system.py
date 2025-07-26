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



movies_dict = pickle.load(open('movies_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)

# Try to load similarity matrix
try:
    # First try regular .pkl file
    with open('similarity.pkl', 'rb') as f:
        similarity = pickle.load(f)
except FileNotFoundError:
    try:
        # If regular file doesn't exist, try .gz
        import gzip
        with gzip.open('similarity.pkl.gz', 'rb') as f:
            similarity = pickle.load(f)
    except gzip.BadGzipFile:
        st.error("The similarity.pkl.gz file is corrupted. Please provide a valid similarity matrix file.")
        raise
    except FileNotFoundError:
        st.error("Neither similarity.pkl nor similarity.pkl.gz found. Please provide a similarity matrix file.")
        raise
    except Exception as e:
        st.error(f"Error loading similarity matrix: {str(e)}")
        raise

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

