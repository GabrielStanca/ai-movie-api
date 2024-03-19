import pandas as pd
import numpy as np
from interpret.analizaText import count_genres_in_text
from interpret.cautariFilme import recommend_movies_from_text_all_genres, find_movie_title_in_text
from interpret.cautariFilme import recommend_movies_from_text_any_genre
from interpret.cautariFilme import recommend_movies_from_text
from interpret.cautariFilme import recommend_movies

# Simulating loading of data
# Imagine these are two small extracts from the 'movies.csv' and 'ratings.csv' files of the MovieLens dataset

# Sample movies data
movies_data = {
    'movieId': [1, 2, 3, 4, 5],
    'title': ['Toy Story (1995)', 'Jumanji (1995)', 'Grumpier Old Men (1995)', 'Waiting to Exhale (1995)', 'Father of the Bride Part II (1995)'],
    'genres': ['Adventure|Animation|Children|Comedy|Fantasy', 'Adventure|Children|Fantasy|Action', 'Comedy|Romance', 'Comedy|Drama|Romance', 'Comedy']
}

# Sample ratings data
ratings_data = {
    'userId': [1, 1, 1, 2, 2],
    'movieId': [1, 2, 3, 4, 5],
    'rating': [4.0, 4.0, 4.0, 3.0, 3.0],
    'timestamp': [964982703, 964981247, 964982224, 964983815, 964982931]
}

# Convert to Pandas DataFrames
movies_df = pd.DataFrame(movies_data)
ratings_df = pd.DataFrame(ratings_data)
# Display the first few rows of each DataFrame
movies_df.head(), ratings_df.head()
# Splitting genres into a format that can be used for content-based filtering
# Creating a binary-encoded column for each genre

# First, let's find the unique genres in the dataset
all_genres = set()
for genres in movies_df['genres']:
    all_genres.update(genres.split('|'))

# Create a column for each genre with binary encoding
for genre in all_genres:
    movies_df[genre] = movies_df['genres'].apply(lambda x: 1 if genre in x else 0)

# We'll not use the 'timestamp' column from ratings, so let's drop it
ratings_df.drop('timestamp', axis=1, inplace=True)

# Let's display the updated movies DataFrame to see the binary-encoded genre columns
movies_df.head(), movies_df.columns

from sklearn.metrics.pairwise import cosine_similarity

# Select only the genre columns for the similarity calculation
genre_columns = movies_df.columns[3:]
genre_matrix = movies_df[genre_columns]

# Calculate the cosine similarity matrix
cosine_sim = cosine_similarity(genre_matrix, genre_matrix)

# Convert the cosine similarity matrix to a DataFrame for better readability
cosine_sim_df = pd.DataFrame(cosine_sim, index=movies_df['title'], columns=movies_df['title'])

# Display the cosine similarity matrix for the first 5 movies
#print(cosine_sim_df.iloc[:5, :5])
# print('---->')
# text = "I'm looking for a Jumanji (1995) and a romance  movie."
# textMovie = "I'm looking for a Jumanji (1995) and a romance  movie."
# #textMovie = "Have you seen Jumanji (1995)?"
# counter = count_genres_in_text(text)
# movie_title_found = find_movie_title_in_text(textMovie, movies_df)
# print(counter)
# print(movie_title_found)
#
# if movie_title_found:
#     respuns = recommend_movies(movie_title_found,cosine_sim_df)
#     print(respuns)
# else:
#     print("No movie title found in the text.")
# print('in movie title')
# if counter == 0 and not movie_title_found:
#     print('No genres found in the text.')
# else:
#     raspuns = recommend_movies_from_text_any_genre(text,movies_df)
#     print(raspuns)
#
# print('in genuri')
# print('<----')

# text_query = "I'm looking for a comedy and romance movie."
# print(recommend_movies_from_text(text_query,movies_df),'recommended_movie')
# print(recommend_movies_from_text_any_genre(text_query, movies_df), 'recommend_movies_from_text_any_genre')
# print(recommend_movies_from_text_all_genres(text_query, movies_df), 'recommend_movies_from_text_all_genres')
#
# recommended_movies = recommend_movies("Jumanji (1995)",cosine_sim_df)
# print(recommended_movies)
