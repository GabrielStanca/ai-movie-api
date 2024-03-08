from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import List

from main import recommend_movies

app = FastAPI()

# Define a list of allowed origins for CORS
# You can use '*' to allow all origins or specify allowed origins as needed
origins = [
    "http://localhost:3000",  # Allow your React app origin
    "http://127.0.0.1:3000",
]

# Add CORSMiddleware to the application
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # List of allowed origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/recommendations/{movie_title}", response_model=List[str])
async def get_recommendations(movie_title: str):
    recommendations = recommend_movies(movie_title)
    return recommendations
