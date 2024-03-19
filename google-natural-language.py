from google.cloud import language_v1


def analyze_text_sentiment(text):
    # Initialize the Language client
    client = language_v1.LanguageServiceClient()

    # Prepare the document with the provided text
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)

    # Detect sentiment in the document
    sentiment = client.analyze_sentiment(request={'document': document}).document_sentiment

    # Return the sentiment score and magnitude as a dictionary
    return {"score": sentiment.score, "magnitude": sentiment.magnitude}


# Example usage
text = "I love this movie!"
sentiment_result = analyze_text_sentiment(text)
print(sentiment_result)
