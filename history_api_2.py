import requests

url = 'http://history.muffinlabs.com/date'
response = requests.get(url)
rawData = response.content
print(rawData)
