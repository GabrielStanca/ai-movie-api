import pandas as pd


import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter


movies_data = pd.read_csv('./database/movies.csv')
# Sample ratings data
ratings_data = pd.read_csv('./database/ratings.csv')
tags_data = pd.read_csv('./database/tags.csv')

# Convert to Pandas DataFrames
movies_df = pd.DataFrame(movies_data)
ratings_df = pd.DataFrame(ratings_data)
tags_df = pd.DataFrame(tags_data)
# Display the first few rows of each DataFrame
movies_df.head(), ratings_df.head() , tags_df.head()
# Splitting genres into a format that can be used for content-based filtering
# Creating a binary-encoded column for each genre

# First, let's find the unique genres in the dataset
all_genres = set()
for genres in movies_df['genres']:
    all_genres.update(genres.split('|'))

# Create a column for each genre with binary encoding
for genre in all_genres:
    movies_df[genre] = movies_df['genres'].apply(lambda x: 1 if genre in x else 0)
all_genres_list = list(all_genres)
all_movies_list = list(movies_df['title'])
all_tags = tags_df['tag'].tolist()

print(all_movies_list)
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




# text = "funny drama from Pixar"
# relevant_movies = find_movies_by_keywords_with_ratings(text, tags_df, movies_df, ratings_df)
# print(relevant_movies[['title', 'rating']])

