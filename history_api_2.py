import requests

url = 'http://history.muffinlabs.com/date'
response = requests.get(url, verify=False)
rawData = response.content
print(rawData)
