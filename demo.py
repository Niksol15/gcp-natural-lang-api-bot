from google.cloud import language_v1

# Instantiates a client
client = language_v1.LanguageServiceClient()

# The text to analyze
text = "Putin is evil"
document = language_v1.Document(
    content=text, type_=language_v1.Document.Type.PLAIN_TEXT
)

# Detects the sentiment of the text
sentiment = client.analyze_sentiment(
    request={"document": document}
).document_sentiment

print("Text: {}".format(text))
print("Sentiment: {:.2f}, {:.2f}".format(sentiment.score, sentiment.magnitude))
