from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from main import movies_df, cosine_sim_df, tags_df, ratings_df
from interpret.analizaText import find_movie_title_in_text, count_genres_in_text, get_first_number_from_string
from interpret.cautariFilme import recommend_movies_from_text_any_genre, recommend_movies, \
    find_movies_by_keywords_with_ratings, top_n_movies_by_rating_genre
from interpret.generareText import generate_movie_descriptions,generate_movie_descriptions_without_rating, generate_movie_descriptions_with_genre, get_genre_description, generate_top_movies_intro
app = FastAPI()
from phrases.phrases import templates_keyword_movies_with_rating, templates_movies_with_year, templates_movies_year_genres

# Define a list of allowed origins for CORS
# You can use '*' to allow all origins or specify allowed origins as needed
origins = [
    "http://localhost:3000",  # Allow your React app origin
    "http://127.0.0.1:3000",
    "http://172.20.10.3:3000",
    'http://0.0.0.0:3000'
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
    rating = get_first_number_from_string(movie_title)
    topNFoundedMovies = []
    counter = count_genres_in_text(movie_title)
    movieTitleFound = find_movie_title_in_text(movie_title, movies_df)
    if rating:
        genGasit = recommend_movies_from_text_any_genre(movie_title, movies_df, rating)
        for gen in genGasit['genuri']:
            found = top_n_movies_by_rating_genre(movies_df, ratings_df, n=rating, genre=gen)
            topNFoundedMovies.append(
                {
                    'gen':get_genre_description(gen),
                    'filme':generate_movie_descriptions(found,templates_keyword_movies_with_rating)
                }
            )
        movieKeywords = find_movies_by_keywords_with_ratings(movie_title, tags_df, movies_df, ratings_df,rating)
        movieKeywords = generate_movie_descriptions(movieKeywords, templates_keyword_movies_with_rating)
        if movieTitleFound:
            movieTitleFound = recommend_movies(movieTitleFound, cosine_sim_df,rating)
            movieTitleFound = generate_movie_descriptions_without_rating(movieTitleFound,templates_movies_with_year)
        else:
            movieTitleFound = "No movie title found in the text."
        if counter == 0 and not movieTitleFound:
            genuri = 'No genres found in the text.'
        else:
            genuri = recommend_movies_from_text_any_genre(movie_title, movies_df, rating)
            if genuri != 'No matching genres found for the given text.' :
                genuri = generate_movie_descriptions_with_genre(genuri,templates_movies_year_genres)
            else :
                genuri = 'No genres found in the text.'
        rating = generate_top_movies_intro(rating)
    else:
        movieKeywords = find_movies_by_keywords_with_ratings(movie_title, tags_df, movies_df, ratings_df)
        movieKeywords = generate_movie_descriptions(movieKeywords, templates_keyword_movies_with_rating)
        if movieTitleFound:
            movieTitleFound = recommend_movies(movieTitleFound, cosine_sim_df)
            movieTitleFound = generate_movie_descriptions_without_rating(movieTitleFound,templates_movies_with_year)
        else:
            movieTitleFound = "No movie title found in the text."
        if counter == 0 and not movieTitleFound:
            genuri = 'No genres found in the text.'
        else:
            genuri = recommend_movies_from_text_any_genre(movie_title, movies_df)
            print(genuri)
            if genuri != 'No matching genres found for the given text.':
                genuri = generate_movie_descriptions_with_genre(genuri,templates_movies_year_genres)
            else:
                genuri = 'No genres found in the text.'
    raspuns = {
        'rating':rating,
        'foundedMoviesByRating': topNFoundedMovies,
        'recomandareFilme': movieTitleFound,
        'recomandareGenuri': genuri,
        'movieKeywords': movieKeywords
    }

    return raspuns
