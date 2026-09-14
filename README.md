# Movie Recommendation System

A content-based movie recommendation system that suggests similar movies based on metadata (genres, cast, crew, keywords, overview) using vectorization and cosine similarity. Built with a Streamlit web interface for interactive use.

## Features

- Search or select any movie from the dataset
- Get the top 5 most similar movie recommendations
- View posters fetched live from The Movie Database (TMDB) API
- Click "Information" on any recommended movie to see detailed metadata:
  - Release date, rating, vote count, runtime, status
  - Genres, spoken languages, production companies
  - Budget, revenue, and overview/tagline

## How It Works

1. **Data preparation** (`Vectorization.ipynb`) — Movie metadata from `tmdb_5000_movies.csv` and `tmdb_5000_credits.csv` is cleaned, merged, and combined into a single "tags" field (overview, genres, keywords, cast, crew).
2. **Vectorization** — The combined text is converted into numerical vectors and saved to `vectors.npz`, alongside the processed movie list in `data_movies.csv`.
3. **Recommendation** (`RecomendationSystem.ipynb`) — Cosine similarity between vectors is used to find the movies most similar to a selected title.
4. **Web app** (`App.py`) — A Streamlit app loads the precomputed vectors and dataset, lets the user pick a movie, and displays recommendations with posters and details pulled from the TMDB API.

## Project Structure

```
Movie-Recommendation-System/
├── App.py                     # Streamlit web application
├── Vectorization.ipynb        # Data cleaning and vectorization notebook
├── RecomendationSystem.ipynb  # Recommendation logic / experimentation notebook
├── data_movies.csv            # Processed movie dataset used by the app
├── tmdb_5000_movies.csv       # Raw TMDB movies dataset
├── tmdb_5000_credits.csv      # Raw TMDB credits dataset
├── vectors.npz                # Precomputed feature vectors
└── requirements.txt           # Python dependencies
```

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/241980094-Umair/Movie-Recommendation-System.git
   cd Movie-Recommendation-System
   ```

2. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

   > Note: `App.py` also relies on `pandas`, `numpy`, and `requests`. If you hit import errors, install these as well:
   > ```bash
   > pip install pandas numpy requests
   > ```

## Usage

Run the Streamlit app from the project root:

```bash
streamlit run App.py
```

Then open the local URL Streamlit prints in your terminal (usually `http://localhost:8501`), select or search for a movie, and click **Show Recommendation**.

## API Key

The app fetches posters and movie details from the [TMDB API](https://www.themoviedb.org/documentation/api). It currently uses a hardcoded API key in `App.py`. For your own deployment, it's recommended to:

1. Get a free API key from TMDB.
2. Replace the hardcoded key with an environment variable, e.g.:
   ```python
   import os
   API_KEY = os.environ.get("TMDB_API_KEY")
   ```

## Tech Stack

- **Python**
- **Streamlit** — web app interface
- **scikit-learn** — cosine similarity for recommendations
- **pandas / NumPy** — data handling
- **TMDB API** — posters and movie metadata

## License

No license specified yet. Consider adding one (e.g., MIT) if you plan to share or accept contributions.
