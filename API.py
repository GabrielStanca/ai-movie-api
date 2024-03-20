from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from main import movies_df, cosine_sim_df, tags_df, ratings_df
from interpret.analizaText import find_movie_title_in_text, count_genres_in_text
from interpret.cautariFilme import recommend_movies_from_text_any_genre, recommend_movies, find_movies_by_keywords_with_ratings

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

@app.get("/recommendations/{movie_title}", response_model=object)
async def get_recommendations(movie_title: str):
    print(movie_title)
    counter = count_genres_in_text(movie_title)
    movieTitleFound = find_movie_title_in_text(movie_title, movies_df)
    movieKeywords = find_movies_by_keywords_with_ratings(movie_title, tags_df, movies_df, ratings_df)
    print(movieKeywords)
    if movieTitleFound:
        movieTitleFound = recommend_movies(movieTitleFound, cosine_sim_df)
    else:
        movieTitleFound = "No movie title found in the text."
    if counter == 0 and not movieTitleFound:
        genuri = 'No genres found in the text.'
    else:
        genuri = recommend_movies_from_text_any_genre(movie_title, movies_df)

    raspuns = {
        'recomandareFilme': movieTitleFound,
        'recomandareGenuri': genuri,
        'movieKeywords': movieKeywords
    }

    return raspuns
