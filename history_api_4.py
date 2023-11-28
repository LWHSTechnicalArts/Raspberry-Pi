import requests
from requests import get

url = 'http://history.muffinlabs.com/date'
one_day = get(url).json() 
print (one_day['data']['Events'][-1]['year'],one_day['data']['Events'][-1]['text'])
