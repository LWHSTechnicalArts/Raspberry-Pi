import requests
from requests import get

url = 'http://history.muffinlabs.com/date'
one_day = get(url, verify=False).json()  
print (one_day['data']['Events'][0]['text'])
