import pandas as pd
from nltk import word_tokenize
from nltk.corpus import stopwords

from interpret.analizaText import extract_keywords_genre



def recommend_movies_from_text_all_genres(text, movies_df, top_n=3):
    keywords = extract_keywords_genre(text)
    keyword_to_genre = {'action': 'Action', 'comedy': 'Comedy', 'romance': 'Romance', 'adventure': 'Adventure'}
    genres_matched = [keyword_to_genre[keyword] for keyword in keywords if keyword in keyword_to_genre]

    if not genres_matched:
        return "No matching genres found for the given text."

    # Filter movies that match all of the genres
    matching_movies = movies_df[(movies_df[genres_matched] == 1).all(axis=1)]['title'].tolist()

    if matching_movies:
        return matching_movies[:top_n]  # Return top N matching movies
    else:
        return "No movies found for the given genres."

def recommend_movies_from_text_any_genre(text, movies_df, top_n=3):
    keywords = extract_keywords_genre(text)
    keyword_to_genre = {'action': 'Action', 'comedy': 'Comedy', 'romance': 'Romance', 'adventure': 'Adventure'}
    genres_matched = [keyword_to_genre[keyword] for keyword in keywords if keyword in keyword_to_genre]

    if not genres_matched:
        return "No matching genres found for the given text."

    # Filter movies that match any of the genres
    matching_movies = movies_df[movies_df[genres_matched].sum(axis=1) > 0]['title'].tolist()

    if matching_movies:
        return matching_movies[:top_n]  # Return top N matching movies
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