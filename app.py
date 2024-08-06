import streamlit as st
import pickle
import pandas as pd
import requests

# Set page configuration for fullscreen
st.set_page_config(
    page_title="Movie Recommender System",
    layout="wide"
)

# Function to fetch movie poster
def fetch_poster(movie_id):
    response = requests.get(
        f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=24e1513fe817f5c6bd8bb51cfd6092e2&language=en-US'
    )
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

# Function to recommend movies
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    
    recommended_movies_names = []
    recommended_movies_posters = []
    recommended_movies_ids = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies_ids.append(movie_id)
        recommended_movies_names.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))

    return recommended_movies_names, recommended_movies_posters, recommended_movies_ids

# Function to get movie details from details_df
def get_movie_details(title):
    try:
        movie_details = extra_df[extra_df['title'] == title].iloc[0]
    except IndexError:
        st.error(f"Details for '{title}' not found.")
        return None
    return movie_details

# Load movie data
movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Load extra movie details
extra_df = pd.read_csv('extra.csv')

# Streamlit UI
st.title('Movie Recommender System')

movie_list = movies['title'].values
selected_movie_name = st.selectbox('How would you like to choose?', movie_list)

if st.button('Show Recommendation'):
    recommended_movies_names, recommended_movies_posters, recommended_movies_ids = recommend(selected_movie_name)
    st.session_state.recommended_movies = recommended_movies_names
    st.session_state.recommended_posters = recommended_movies_posters
    st.session_state.selected_movie = None

if 'recommended_movies' in st.session_state:
    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.image(st.session_state.recommended_posters[i])
            st.write(st.session_state.recommended_movies[i])
            if st.button(f"Show details", key=f"btn_{i}"):
                st.session_state.selected_movie = st.session_state.recommended_movies[i]
                
st.markdown("""<br><br>""", unsafe_allow_html=True)

if 'selected_movie' in st.session_state and st.session_state.selected_movie:
    details = get_movie_details(st.session_state.selected_movie)
    if details is not None:
        st.subheader(f"Details of '{details['title']}' movie:")
        st.write(f"'Release Date' :  {details['release_date']}")
        st.write(f"'Categories type' :  {', '.join(eval(details['genres']))}")
        st.write(f"'Time' :  {details['runtime']} hours")
        st.write(f"'Rating' :  {details['vote_average']}")
        st.write(f"'Overview' :  {details['overview']}")
        st.write(f"'Actors & Actress' :  {', '.join(eval(details['cast']))}")
        st.write(f"'Team' :  {', '.join(eval(details['crew']))}")
