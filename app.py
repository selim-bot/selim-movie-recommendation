import streamlit as st
import pickle
import requests
import pandas as pd
import time  # otional delay


# Backgound
def set_background(url):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("{url}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

background_url = "https://images.unsplash.com/photo-1524985069026-dd778a71c7b4?auto=format&fit=crop&w=1470&q=80"
set_background(background_url)


# Load
movies_list = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))


# Fetch poster from TMDb API
def fetch_poster(movie_id):
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US'
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        poster_path = data.get('poster_path')
        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path
        else:
            return "https://via.placeholder.com/500x750?text=No+Image"
    except requests.exceptions.RequestException as e:
        print(f"Error fetching poster for movie {movie_id}: {e}")
        return "https://via.placeholder.com/500x750?text=No+Image"


# Recommendation function
def recommend(movie):
    movie_index = movies_list[movies_list['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_indices = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movie_posters = []

    for i in movie_indices:
        movie_id = movies_list.iloc[i[0]].movie_id
        recommended_movies.append(movies_list.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_poster(movie_id))
        time.sleep(0.2)  # optional: small delay to avoid hitting API too fast

    return recommended_movies, recommended_movie_posters

# Streamlt

st.title('🎬 Movie Recommender System')

movie_titles = movies_list['title'].tolist()
selected_movie_name = st.selectbox("Select a movie to get recommendations:", movie_titles)

if st.button('Recommend'):
    recommended_movies, recommended_movie_posters = recommend(selected_movie_name)
    st.subheader("Recommended Movies:")
    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.text(recommended_movies[i])
            st.image(recommended_movie_posters[i])
