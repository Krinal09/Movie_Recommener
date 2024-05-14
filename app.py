import streamlit as st
import pickle
import pandas as pd
import requests


# this is for when we have ipynb file in our main file

# and this is a best tric
# movies_list = pickle.load(open('movies.pkl','rb'))
# movies_list = movies_list['title'].values


def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=6d28be3a422730d8cb2a6897189d4355&language=en-US'.format(movie_id)) 
    
    data = response.json()
    return " https://image.tmdb.org/t/p/w500/" + data['poster_path']

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)),reverse=True, key= lambda x:x[1])[1:6]
    
    recommended_movies_names = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
      
        recommended_movies_names.append(movies.iloc[i[0]].title)
          # pest poster from API
        recommended_movies_posters.append(fetch_poster(movie_id))

    return recommended_movies_names,recommended_movies_posters


st.title('Movie Recommender System')
movies_dict = pickle.load(open('movies_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl','rb'))

movie_list = movies['title'].values

selected_movie_name = st.selectbox(
    'How would you like to choose?',
    movies['title'].values
)

if st.button('Show Recommendation'):
    recommended_movies_names,recommended_movies_posters = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movies_names[0])
        st.image(recommended_movies_posters[0])
    with col2:
        st.text(recommended_movies_names[1])
        st.image(recommended_movies_posters[1])
    with col3:
        st.text(recommended_movies_names[2])
        st.image(recommended_movies_posters[2])
    with col4:
        st.text(recommended_movies_names[3])
        st.image(recommended_movies_posters[3])
    with col5:
        st.text(recommended_movies_names[4])
        st.image(recommended_movies_posters[4])