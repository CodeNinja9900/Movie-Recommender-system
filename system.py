import pandas as pd
import requests
import  streamlit as st
import pickle

def fetch_postel(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=fec312a4d375bf2a15e1bac80c05df2d'.format(movie_id))
    data = response.json()
    print(data)
    return "https://image.tmdb.org/t/p/w500"+data['poster_path']



def recommended(movie):
    movie_index = movies[movies ['title'] == movie].index[0]
    distance = similarity[movie_index]
    movie_list = sorted(list(enumerate(distance)), reverse=True, key=lambda x:x[1])[1:6]

    recommended_movie = []
    recommended_movie_posters = []
    for i in movie_list:
        movie_id = movies.iloc[i[0]].id
        recommended_movie.append(movies.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_postel(movie_id))
        print(movies.iloc[i[0]].title)
    return  recommended_movie, recommended_movie_posters



movies_dict = pickle.load(open('movies_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl','rb'))

st.title('movie recommender system')

selected_movie_name = st.selectbox(
 'Search for your favourite movies',
    movies['title'].values
)

if st.button('recommded'):
    names, posters = recommended(selected_movie_name)  # ignore the 3rd value

    col1, col2, col3, col4, col5 = st.columns(5)

    # Populate each column dynamically
    with col1:
        st.markdown(names[0])
        st.image(posters[0])
    with col2:
        st.markdown(names[1])
        st.image(posters[1])
    with col3:
        st.markdown(names[2])
        st.image(posters[2])
    with col4:
        st.markdown(names[3])
        st.image(posters[3])
    with col5:
        st.markdown(names[4])
        st.image(posters[4])

