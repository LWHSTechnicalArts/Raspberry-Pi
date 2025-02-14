import requests
from gpiozero import LED
import time

led_warm = LED(17)
led_cold = LED(18)

settings = {
    'api_key':'Your API Key',
    'zip_code':'94112',
    'country_code':'us',
    'temp_unit':'imperial'} #unit can be metric, imperial, or kelvin

BASE_URL = "http://api.openweathermap.org/data/2.5/weather?appid={0}&zip={1},{2}&units={3}"

while True:
    final_url = BASE_URL.format(settings["api_key"],settings["zip_code"],settings["country_code"],settings["temp_unit"])
    weather_data = requests.get(final_url).json()
    temperature = weather_data["main"]["temp"]  
    print(temperature)

    if(temperature<=57):
        led_cold.on()
        led_warm.off()
    else:
        led_cold.off()
        led_warm.on()
    
    time.sleep(120) #get new data every 120 seconds
