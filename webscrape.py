import requests
from bs4 import BeautifulSoup

def scrape_text(url):
    try:
        # Send a GET request to the webpage
        response = requests.get(url)
        response.raise_for_status()  # Raises an error for bad status codes

        # Parse the HTML content of the page
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find all paragraph tags and extract text (as an example)
        paragraphs = soup.find_all('h2')
        for paragraph in paragraphs:
            print(paragraph.get_text())

    except requests.RequestException as e:
        print(f"Error during requests to {url} : {e}")

# URL of the webpage you want to scrape
url = 'https://design-milk.com'

scrape_text(url)