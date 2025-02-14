import requests

url = 'http://history.muffinlabs.com/date'
response = requests.get(url, verify=False)
print(response)
