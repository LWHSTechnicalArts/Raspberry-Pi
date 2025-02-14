import requests
from requests import get

url = 'http://history.muffinlabs.com/date/12/25'
one_day = get(url, verify=False).json() 
print (one_day['data']['Events'][-1]['year'],one_day['data']['Events'][-1]['text'])
