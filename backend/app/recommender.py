import os
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

from .models import RecommendationResponseItem
from .preprocess import preprocess_history, load_process_data


MODEL_NAME = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")


class Recommender:
    def __init__(self, imdb_csv: str, netflix_titles_csv: str, model_name: str = MODEL_NAME):
        self.model = SentenceTransformer(model_name)
        self.imdb_csv = imdb_csv
        self.netflix_titles_csv = netflix_titles_csv
        self.catalog = None  # lazy load

    def recommend_from_csv(self, netflix_csv: str, top_k: int = 20):
        """
        End-to-end pipeline:
        - Preprocess Netflix history
        - Build user profile embedding
        - Compare against catalog
        - Return top recommendations
        """

        imdb_df, netflix_titles_df = load_process_data(self.imdb_csv, self.netflix_titles_csv)

        if self.catalog is None:
            # combine both datasets
            self.catalog = pd.concat([imdb_df, netflix_titles_df]).drop_duplicates(subset=["title"]).reset_index(drop=True)

        # 1. Preprocess Netflix history
        user_df = preprocess_history(netflix_csv, imdb_df, netflix_titles_df)
        if user_df.empty:
            return []
        
        print(f"User has {len(user_df)} unique titles after preprocessing.")

        # 2. Build user profile embedding
        user_texts = [
            f"{row['title']} {row.get('plot','')} {row.get('genre','')} {row.get('director','')}"
            for _, row in user_df.iterrows()
        ]
        user_embs = self.model.encode(user_texts)
        profile = np.mean(user_embs, axis=0, keepdims=True)

        # 3. Prepare candidate pool
        cand_texts = [
            f"{row['title']} {row.get('plot','')} {row.get('genre','')} {row.get('director','')}"
            for _, row in self.catalog.iterrows()
        ]
        cand_embs = self.model.encode(cand_texts)

        # 4. Compute similarities
        sims = cosine_similarity(profile, cand_embs)[0]
        idxs = np.argsort(sims)[::-1]

        # 5. Build recommendations list
        recs = []
        for i in idxs[:top_k]:
            row = self.catalog.iloc[i]
            recs.append(
                RecommendationResponseItem(
                    title=row["title"],
                    genre=row.get("genre", ""),
                    director=row.get("director", ""))
            )
        return recs
