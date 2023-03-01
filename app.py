import streamlit as st
import pickle
import pandas as pd
import requests


def fetch_poster(movie_id):
    res = requests.get(
        'https://api.themoviedb.org/3/movie/{}]?api_key=21bed29ace19a95f9ee5790b2d5615b0&language=en-US'.format(
            movie_id))
    data = res.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']


# get function from notebook and make changes
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = similarity[index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:11]

    recommended_movies = []
    movie_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)

        # getting the posters from tmdb API
        movie_posters.append(fetch_poster(movie_id))
    return recommended_movies, movie_posters


movie_names = pickle.load(open('movies.pkl', 'rb'))
movies = pd.DataFrame(movie_names)

similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Movie Recommender System')

option = st.selectbox(
    'Choose a movie',
    movies['title'].values,
)


if option != "":

    # st.write(option)
    names, posters = recommend(option)

    col1, col2, col3, col4, col5 = st.columns(5)
    col_list = [col1, col2, col3, col4, col5]

    for i in range(10):
        if i > 4:
            with col_list[i-5]:
                st.image(posters[i])
                st.write(names[i])
        else:
            with col_list[i]:
                st.image(posters[i])
                st.write(names[i])
                if len(names[i]) < 20:
                    st.write(" ")

