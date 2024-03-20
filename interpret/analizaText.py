import nltk
import re
from nltk import word_tokenize
from nltk.corpus import stopwords


nltk.download('punkt')
nltk.download('stopwords')


def find_movie_title_in_text(text, movies_df):
    # Normalize the text for better matching
    normalized_text = text.lower()

    # Compile a regular expression pattern to extract title and year
    title_pattern = re.compile(r"(.*)\s\((\d{4})\)")

    # Iterate over the movie titles to check for a match
    for title in movies_df['title']:
        # Attempt to match the title pattern to extract title and year
        match = title_pattern.match(title)

        if match:
            # If there's a match, separate the title and year
            normalized_title, year = match.groups()
            normalized_title = normalized_title.lower()
        else:
            # If no year is present, use the whole title
            normalized_title = title.lower()
            year = ""

        # Check if the normalized movie title is in the normalized text
        # Additionally, check if the year is either present in the text or irrelevant
        if normalized_title in normalized_text and (year in normalized_text or not year):
            return title  # Return the original title

    # If no movie title is found in the text, return None
    return None



def extract_keywords_genre(text):
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(text)
    # Filter out stop words and return keywords
    keywords = [word for word in word_tokens if not word in stop_words and word.isalpha()]
    return keywords


def count_genres_in_text(text):
    # Extract keywords from the input text
    keywords = extract_keywords_genre(text)

    # Define your mapping from keywords to genres
    keyword_to_genre = {'action': 'Action', 'comedy': 'Comedy', 'romance': 'Romance', 'adventure': 'Adventure'}

    # Extract genres based on the keywords found
    genres = {keyword_to_genre[keyword] for keyword in keywords if keyword in keyword_to_genre}

    # Count the number of unique genres mentioned
    num_genres = len(genres)

    return num_genres
