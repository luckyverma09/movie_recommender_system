import pickle
import streamlit as st
import pandas as pd
import requests

# Function to fetch movie poster
def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=26d6ea2985ea4bb038a69fcb672b4819'.format(movie_id))
    data = response.json()
    poster_path = data.get('poster_path')
    
    return "https://image.tmdb.org/t/p/w500/" + poster_path
    

# Function to recommend similar movies
def recommend(movie, movies_df, similarity_matrix):
    movie_index = movies_df[movies_df['title'] == movie].index[0]
    distances = similarity_matrix[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movie_names = []
    recommended_movie_posters = []
    for i in movies_list:
        movie_id = movies_df.iloc[i[0]].movie_id
        recommended_movie_names.append(movies_df.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_poster(movie_id))
    return recommended_movie_posters, recommended_movie_names

# Load data and models
movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Streamlit UI
st.title('Movie Recommender System')

selected_movie_name = st.selectbox('Select a movie', movies['title'].values)

if st.button('Recommend'):
    recommended_movie_posters, recommended_movie_names = recommend(selected_movie_name, movies, similarity)
    cols = st.columns(5)
    for i, col in enumerate(cols):
        col.text(recommended_movie_names[i])
        col.image(recommended_movie_posters[i])