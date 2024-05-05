import pandas as pd
from nltk import word_tokenize
from nltk.corpus import stopwords
from main import all_genres_list
from interpret.analizaText import extract_keywords_genre



def recommend_movies_from_text_any_genre(text, movies_df, top_n=3):
    # Extract potential keywords that could correspond to genres from the text
    keywords = extract_keywords_genre(text)  # Assuming this function returns a list of keywords found in text

    # Convert keywords to genres using a more dynamic mapping that includes all possible genres
    keyword_to_genre = {genre.lower(): genre for genre in all_genres_list}  # Mapping from genre keywords to genres
    # Find which genres are matched in the keywords extracted
    genres_matched = [keyword_to_genre[keyword] for keyword in keywords if keyword.lower() in keyword_to_genre]

    if not genres_matched:
        return "No matching genres found for the given text."

    # Create a boolean DataFrame where each cell is True if the movie belongs to the genre
    is_genre = movies_df['genres'].apply(lambda x: any(genre in x for genre in genres_matched))

    # Filter movies that match any of the genres
    matching_movies = movies_df[is_genre]['title'].tolist()

    if matching_movies:
        return {'genuri': genres_matched , 'filme': matching_movies[:top_n]}  # Return top N matching movies
    else:
        return "No movies found for the given genres."

def find_movies_by_keywords_with_ratings(text, tags_df, movies_df, ratings_df, top_n=3):
    # Tokenize the text into words
    words = word_tokenize(text.lower())

    # Filter out stopwords
    stop_words = set(stopwords.words('english'))
    filtered_words = [word for word in words if word.isalnum() and word not in stop_words]

    # Convert filtered words into a set for efficient searching
    keywords_set = set(filtered_words)

    # Find unique movieIds where the tag matches any of the keywords
    matching_movie_ids = tags_df[tags_df['tag'].str.lower().apply(lambda tag: any(keyword in tag.split() for keyword in keywords_set))]['movieId'].unique()

    # Retrieve the movies that match the found movieIds
    matching_movies = movies_df[movies_df['movieId'].isin(matching_movie_ids)]

    # Calculate the average rating for each movie
    average_ratings = ratings_df.groupby('movieId')['rating'].mean().reset_index()

    # Merge the matching movies with their average ratings
    matching_movies_with_ratings = pd.merge(matching_movies, average_ratings, on='movieId', how='left')

    # Sort the movies by average rating in descending order
    matching_movies_sorted = matching_movies_with_ratings.sort_values(by='rating', ascending=False)

    movies_list = matching_movies_sorted[['movieId', 'title', 'rating']].to_dict(orient='records')


    return movies_list[:top_n]

def recommend_movies(movie_title, cosine_sim_matrix, top_n=3):
    # Check if the movie exists in the cosine similarity matrix
    if movie_title not in cosine_sim_matrix.index:
        return "Movie not found in the dataset."

    # Get the similarity scores for the input movie with all other movies
    sim_scores = cosine_sim_matrix[movie_title]

    # Sort the movies based on the similarity scores in descending order
    sim_scores_sorted = sim_scores.sort_values(ascending=False)

    # Get the titles of the top N most similar movies, excluding the first one (the movie itself)
    top_similar_titles = sim_scores_sorted.iloc[1:top_n + 1].index.tolist()

    # Return the top N most similar movies
    return top_similar_titles

def top_n_movies_by_rating_genre(movies_df, ratings_df, n=3, genre=None):
    # Calculate the average rating for each movie
    average_ratings = ratings_df.groupby('movieId')['rating'].mean().reset_index()

    # Merge the average ratings with the movies DataFrame to get titles and genres
    movies_with_ratings = pd.merge(average_ratings, movies_df, on='movieId')

    # Filter by genre if specified
    if genre:
        movies_with_ratings = movies_with_ratings[movies_with_ratings['genres'].str.contains(genre, case=False, na=False)]

    # Sort the movies by average rating in descending order
    sorted_movies = movies_with_ratings.sort_values(by='rating', ascending=False)

    # Select the top n movies
    top_n = sorted_movies.head(n)

    # Format the result for display or further processing
    top_n_movies_info = top_n[['title', 'rating']].to_dict(orient='records')

    return top_n_movies_info