import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

def analyze_sentiment(text):
    sia = SentimentIntensityAnalyzer()
    sentiment = sia.polarity_scores(text)
    return sentiment

if __name__ == "__main__":
    text = input("Enter a sentence for sentiment analysis: ")
    sentiment = analyze_sentiment(text)
    print("Sentiment Analysis:", sentiment)