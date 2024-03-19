from interpret.analizaText import extract_keywords


def find_movie_title_in_text(text, movies_df):
    # Normalize the text for better matching
    normalized_text = text.lower()

    # Iterate over the movie titles to check for a match
    for title in movies_df['title']:
        # Normalize the movie title
        normalized_title = title.lower()

        # Check if the normalized movie title is in the normalized text
        if normalized_title in normalized_text:
            return title  # Return the original title

    # If no movie title is found in the text, return None
    return None


def recommend_movies_from_text(text, movies_df):
    keywords = extract_keywords(text)
    keyword_to_genre = {'action': 'Action', 'comedy': 'Comedy', 'romance': 'Romance',
                        'adventure': 'Adventure'}  # Ensure these match your DataFrame's columns
    genres = [keyword_to_genre[keyword] for keyword in keywords if keyword in keyword_to_genre]

    if not genres:
        return "No matching genres found for the given text."

    genre = genres[0]  # For simplicity, just take the first genre matched for demonstration

    # Check if the genre exists in the DataFrame columns
    if genre not in movies_df.columns:
        return f"No movies found for the genre: {genre}."

    movies_matching_genre = movies_df[movies_df[genre] == 1]['title'].tolist()

    if movies_matching_genre:
        return movies_matching_genre[0]  # Return the first movie that matches the genre
    else:
        return "No movies found for the given genres."

def recommend_movies_from_text_all_genres(text, movies_df, top_n=3):
    keywords = extract_keywords(text)
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
    keywords = extract_keywords(text)
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