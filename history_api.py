import requests

url = 'http://history.muffinlabs.com/date'
response = requests.get(url)
print(response)
