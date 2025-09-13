from pydantic import BaseModel

class RecommendationResponseItem(BaseModel):
    title: str
    genre: str
    director: str
