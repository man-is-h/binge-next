import os
import pandas as pd
from .utils import normalize_title, deduplicate_titles


def load_process_data(imdb_csv: str, netflix_titles_csv: str):
    """Load and preprocess both datasets."""
    base_path = os.path.dirname(__file__)
    data_path = os.path.join(base_path, "data")

    imdb_csv = os.path.join(data_path, imdb_csv)
    netflix_titles_csv = os.path.join(data_path, netflix_titles_csv)
    
    cols = ["title", "genre", "plot", "director"]

    imdb_df = pd.read_csv(imdb_csv)
    imdb_df = imdb_df.rename(columns={
        "Series_Title": "title", 
        "Genre": "genre", 
        "Overview": "plot", 
        "Director": "director"
        })
    imdb_df = imdb_df[cols]
    imdb_df["norm_title"] = imdb_df["title"].str.lower().str.strip()
    imdb_df.fillna('', inplace=True)

    netflix_df = pd.read_csv(netflix_titles_csv, encoding='latin1')
    netflix_df = netflix_df.rename(columns={
        "listed_in": "genre", 
        "description": "plot", 
        "Director": "director"})
    netflix_df = netflix_df[cols]
    netflix_df["norm_title"] = netflix_df["title"].str.lower().str.strip()
    netflix_df.fillna('', inplace=True)

    return imdb_df, netflix_df

def preprocess_history(netflix_csv: str, imdb_df: pd.DataFrame, netflix_titles_df: pd.DataFrame):
    """
    Full preprocessing pipeline:
    - Load Netflix history
    - Deduplicate series/episodes
    - Match against IMDb/Netflix dataset
    """

    # Create lookup dictionaries for fast matching
    # The 'records' orientation is a list of dicts, perfect for this.
    imdb_lookup = {row['norm_title']: row for row in imdb_df.to_dict('records')}
    netflix_lookup = {row['norm_title']: row for row in netflix_titles_df.to_dict('records')}

    # 1. Load Netflix viewing history
    history = pd.read_csv(netflix_csv)
    raw_titles = history["Title"].tolist()

    # 2. Deduplicate
    deduped_titles = deduplicate_titles(raw_titles)

    # 3. Try to resolve each title
    results = []
    for title in deduped_titles:
        norm = normalize_title(title)

        # Check IMDb dataset first (O(1) average lookup)
        match = imdb_lookup.get(norm)
        if match:
            results.append({
                "title": match.get("title"),
                "genre": match.get("genre", ""),
                "plot": match.get("plot", ""),
                "director": match.get("director", ""),
                "source": "imdb_catalog"
            })
            continue

        # Then check Netflix dataset (O(1) average lookup)
        match_netflix = netflix_lookup.get(norm)
        if match_netflix:
            results.append({
                "title": match_netflix.get("title"),
                "genre": match_netflix.get("genre", ""),
                "plot": match_netflix.get("plot", ""),
                "director": match_netflix.get("director", ""),
                "source": "netflix_titles"
            })
            continue

    return pd.DataFrame(results)

