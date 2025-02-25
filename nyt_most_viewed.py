from requests import get

url = "https://api.nytimes.com/svc/mostpopular/v2/viewed/1.json?api-key=zRolWqHVCFNkXcaOrrvUCz61Eg6Cn0ns"

# Fetch data with a User-Agent header (to prevent blocks)
headers = {"User-Agent": "Mozilla/5.0"}
response = get(url, headers=headers).json()

# Extract and print the top 5 article titles
if "results" in response:
    for article in response["results"][:5]:  # Get up to 5 articles safely
        print(article["title"])
else:
    print("Error: No results found")
