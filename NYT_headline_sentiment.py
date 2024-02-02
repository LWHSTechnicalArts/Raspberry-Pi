import requests
from textblob import TextBlob

# Fetch headlines
api_key = '9fOBZYU0RnUdvRbunt57BBhvNPDzaTdX'  # Replace with your NYT API key
url = f'https://api.nytimes.com/svc/topstories/v2/home.json?api-key={api_key}'
response = requests.get(url)
top_stories = response.json()
headlines = [story['title'] for story in top_stories['results']]

# Analyze sentiment
for headline in headlines:
    sentiment = TextBlob(headline).sentiment
    print(f'Headline: {headline}\nSentiment: Polarity={sentiment.polarity}, Subjectivity={sentiment.subjectivity}\n')
