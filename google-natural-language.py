from google.cloud import language_v1
from main import movies_df, all_genres_list, all_tags, all_movies_list
import os

cred_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
print(f"The credential path is set to: {cred_path}")

def analyze_text_sentiment(text):
    # Initialize the Language client
    client = language_v1.LanguageServiceClient()

    # Prepare the document with the provided text
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)

    # Detect sentiment in the document
    sentiment = client.analyze_sentiment(request={'document': document}).document_sentiment

    # Return the sentiment score and magnitude as a dictionary
    return {"score": sentiment.score, "magnitude": sentiment.magnitude}



def interpret_request(text):
    # Lowercase the text for easier comparison
    lower_text = text.lower()
    print()
    # Try to find a genre in the text
    requested_genre = next((genre for genre in all_genres_list if genre.lower() in lower_text), None)

    # Try to find a specific key in the text
    specific_key = next((keyword for keyword in all_tags if keyword.lower() in lower_text), None)

    # Try to find a movie in the text
    specific_movie = next((movie for movie in all_movies_list if movie.lower() in lower_text), None)

    # Analyze the sentiment of the text
    sentiment_result = analyze_text_sentiment(text)

    # Interpret sentiment scores
    sentiment = 'positive' if sentiment_result['score'] > 0 else 'negative' if sentiment_result['score'] < 0 else 'neutral'

    # Formulate response based on the detected genre, keyword, and sentiment
    print('requested_genre')
    print(requested_genre)
    print('specific_key')
    print(specific_key)
    print('specific_movie')
    print(specific_movie)
    if requested_genre and specific_key:
        response = f"Fetching {requested_genre} movies related to {specific_key} with a {sentiment} sentiment."
    elif requested_genre:
        response = f"Looking for {requested_genre} movies with a {sentiment} sentiment."
    elif specific_key:
        response = f"Searching for movies related to {specific_key} with a {sentiment} sentiment."
    else:
        response = "Understanding your preferences."

    return response



text = "I would like a movie but nothing with Action and star wars"
print('user: ' + text )
interpretation = interpret_request(text)
print('ai: ' + interpretation)

# Example usage
text = "I would like a movie with action Jumanji: Welcome to the Jungle"
print('user: ' + text)
interpretation = interpret_request(text)
print('ai: ' + interpretation)

