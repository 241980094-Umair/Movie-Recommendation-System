import pickle
import pandas as pd
import requests
import streamlit as st
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

API_KEY = "8265bd1679663a7ea12ac168da84d2e8"

movies = pd.read_csv("data_movies.csv")

data = np.load("vectors.npz")
vectors = data["vectors"]


def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"

    try:
        response = requests.get(url)
        data = response.json()

        poster_path = data.get("poster_path")

        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path

    except Exception:
        pass

    return "https://via.placeholder.com/500x750?text=No+Poster"


def fetch_movie_details(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"

    try:
        response = requests.get(url)
        return response.json()

    except Exception:
        return None


def recommend(movie):
    index = movies[movies["title"] == movie].index[0]

    similarity = cosine_similarity(
        vectors[index:index + 1],
        vectors
    )[0]

    distances = sorted(
        list(enumerate(similarity)),
        reverse=True,
        key=lambda x: x[1]
    )

    recommended_movie_names = []
    recommended_movie_posters = []
    recommended_movie_ids = []

    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id

        recommended_movie_ids.append(movie_id)
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(
            movies.iloc[i[0]].title
        )

    return (
        recommended_movie_names,
        recommended_movie_posters,
        recommended_movie_ids
    )


def show_movie_details(movie_id):
    data = fetch_movie_details(movie_id)

    if data is None:
        st.error("Unable to fetch movie information.")
        return

    poster_path = data.get("poster_path")

    if poster_path:
        poster_url = "https://image.tmdb.org/t/p/w500/" + poster_path
    else:
        poster_url = "https://via.placeholder.com/500x750?text=No+Poster"

    st.title(data.get("title", "Unknown"))

    col1, col2 = st.columns([1, 2])

    with col1:
        st.image(poster_url)

    with col2:
        st.subheader("Movie Information")

        st.write(
            "**Release Date:**",
            data.get("release_date", "N/A")
        )

        st.write(
            "**Rating:**",
            data.get("vote_average", "N/A")
        )

        st.write(
            "**Votes:**",
            data.get("vote_count", "N/A")
        )

        st.write(
            "**Runtime:**",
            f"{data.get('runtime', 'N/A')} minutes"
        )

        st.write(
            "**Status:**",
            data.get("status", "N/A")
        )

        st.write(
            "**Original Language:**",
            data.get("original_language", "N/A")
        )

        genres = data.get("genres", [])

        if genres:
            genre_names = ", ".join(
                genre["name"] for genre in genres
            )
        else:
            genre_names = "N/A"

        st.write("**Genres:**", genre_names)

        st.write(
            "**Popularity:**",
            data.get("popularity", "N/A")
        )

    st.subheader("Overview")

    st.write(
        data.get(
            "overview",
            "No overview available."
        )
    )

    if data.get("tagline"):
        st.subheader("Tagline")
        st.write(data["tagline"])

    st.subheader("Additional Details")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Budget",
            f"${data.get('budget', 0):,}"
        )

    with col2:
        st.metric(
            "Revenue",
            f"${data.get('revenue', 0):,}"
        )

    with col3:
        st.metric(
            "Vote Average",
            data.get("vote_average", "N/A")
        )

    production_companies = data.get(
        "production_companies",
        []
    )

    if production_companies:
        st.subheader("Production Companies")

        company_names = ", ".join(
            company["name"]
            for company in production_companies
        )

        st.write(company_names)

    spoken_languages = data.get(
        "spoken_languages",
        []
    )

    if spoken_languages:
        st.subheader("Spoken Languages")

        languages = ", ".join(
            language["english_name"]
            for language in spoken_languages
        )

        st.write(languages)


st.header("Movie Recommendation System")

movie_list = movies["title"].values

selected_movie = st.selectbox(
    "Type or select a movie",
    movie_list
)

if st.button("Show Recommendation"):

    names, posters, movie_ids = recommend(selected_movie)

    st.session_state["recommendations"] = {
        "names": names,
        "posters": posters,
        "ids": movie_ids
    }

if "recommendations" in st.session_state:

    names = st.session_state["recommendations"]["names"]
    posters = st.session_state["recommendations"]["posters"]
    movie_ids = st.session_state["recommendations"]["ids"]

    st.subheader("Recommended Movies")

    cols = st.columns(5)

    for idx, col in enumerate(cols):

        with col:

            st.image(posters[idx])

            st.write(names[idx])

            if st.button(
                "Information",
                key=f"info_{movie_ids[idx]}"
            ):

                st.session_state["selected_movie_id"] = movie_ids[idx]

if "selected_movie_id" in st.session_state:

    st.divider()

    show_movie_details(
        st.session_state["selected_movie_id"]
    )