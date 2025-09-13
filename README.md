# Cross-Platform Movie Recommender

This repository implements a full-stack project that:
- Accepts a user's **Netflix viewing history CSV** upload.
- Enriches titles using IMDB and Netflix datasets.
- Builds item embeddings and a content-based + popularity hybrid recommender.
- Recommends movies/TV shows.
- Provides a small React front-end to upload the CSV and view recommendations.

## Quick start (local)

1. Build and run with docker-compose:
    ```
    docker-compose up --build
    ```
2. Frontend: http://localhost:3000  Backend: http://localhost:8000

## Notes
- The project uses the following kaggle datasets:
    - https://www.kaggle.com/datasets/harshitshankhdhar/imdb-dataset-of-top-1000-movies-and-tv-shows
    - https://www.kaggle.com/datasets/rahulvyasm/netflix-movies-and-tv-shows
- `sentence-transformers` downloads models the first time you run the backend; this may take a couple of minutes.
