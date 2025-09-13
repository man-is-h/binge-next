import os
import shutil
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from .recommender import Recommender
from .models import RecommendationResponseItem

app = FastAPI(title='BingeNext', version='0.1.0')

# Add CORS middleware
origins = [
    "http://localhost",
    "http://localhost:3000", # Default for create-react-app
    "http://localhost:5173", # Default for Vite
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize recommender once with IMDb dataset
IMDB_CSV = "imdb_top_1000.csv"
NETFLIX_TITLES_CSV = "netflix_titles.csv"
recommender = Recommender(imdb_csv=IMDB_CSV, netflix_titles_csv=NETFLIX_TITLES_CSV)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/recommend", response_model=list[RecommendationResponseItem])
async def recommend(file: UploadFile = File(...), top_k: int = 10):
    """
    Upload NetflixViewingHistory.csv and get movie/show recommendations.
    """
    # Save uploaded file temporarily
    tmp_path = f"tmp_{file.filename}"
    with open(tmp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        # Run recommendation pipeline
        recs = recommender.recommend_from_csv(tmp_path, top_k=top_k)
    
        # Return an explicit JSON response
        return recs
    finally:
        # Clean up temp file
        os.remove(tmp_path)
