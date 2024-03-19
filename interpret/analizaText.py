import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords


nltk.download('punkt')
nltk.download('stopwords')


def extract_keywords(text):
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(text)
    # Filter out stop words and return keywords
    keywords = [word for word in word_tokens if not word in stop_words and word.isalpha()]
    return keywords


def count_genres_in_text(text):
    # Extract keywords from the input text
    keywords = extract_keywords(text)

    # Define your mapping from keywords to genres
    keyword_to_genre = {'action': 'Action', 'comedy': 'Comedy', 'romance': 'Romance', 'adventure': 'Adventure'}

    # Extract genres based on the keywords found
    genres = {keyword_to_genre[keyword] for keyword in keywords if keyword in keyword_to_genre}

    # Count the number of unique genres mentioned
    num_genres = len(genres)

    return num_genres

    # if num_genres == 0:
    #     return "No genres found in the text."
    # elif num_genres == 1:
    #     return f"One genre found: {genres.pop()}"
    # else:
    #     return f"Multiple genres found: {', '.join(genres)}"
