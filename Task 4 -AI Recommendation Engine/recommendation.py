import pandas as pd
import ast
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

# Load dataset
movies = pd.read_csv('movies_metadata.csv', low_memory=False)

# Keep only title and genres
movies = movies[['title', 'genres']].dropna()

# Convert genres JSON-like string to plain text
def parse_genres(x):
    try:
        genres_list = ast.literal_eval(x)
        return ' '.join([g['name'] for g in genres_list])
    except:
        return ''

movies['genres'] = movies['genres'].apply(parse_genres)

# TF-IDF on genres
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(movies['genres'])

# Create lowercase index mapping for case-insensitive search
indices_lower = pd.Series(movies.index, index=movies['title'].str.lower()).drop_duplicates()

def get_recommendations(title, top_n=5):
    # Case-insensitive title lookup
    title_lower = title.lower()
    if title_lower not in indices_lower:
        return []

    idx = indices_lower[title_lower]
    
    # Compute similarity for only the requested movie
    sim_scores = linear_kernel(tfidf_matrix[idx], tfidf_matrix).flatten()
    
    # Get top N scores (excluding the movie itself)
    sim_indices = sim_scores.argsort()[-top_n-1:-1][::-1]
    
    return movies['title'].iloc[sim_indices].tolist()
