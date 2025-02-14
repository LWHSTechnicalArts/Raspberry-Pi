import time
import random
import requests
from requests import get

url = 'http://history.muffinlabs.com/date'

while True:
  item = random.randint(-10,10)
  one_day = get(URL, verify=False).json()
  print (one_day['data']['Events'][item]['year'],one_day['data']['Events'][item]['text'])
  time.sleep(20)
