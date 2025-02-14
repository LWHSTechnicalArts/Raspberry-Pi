import time
import random
from requests import get

url = 'http://history.muffinlabs.com/date'

while True:
  item = random.randint(-10,10)
  one_day = get(url, verify=False).json()
  print (one_day['data']['Events'][item]['year'],one_day['data']['Events'][item]['text'])
  time.sleep(20)
