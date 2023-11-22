"""
Basic `AHTx0` example test
"""

import time
import board
import adafruit_ahtx0

# Create sensor object, communicating over the board's default I2C bus
i2c = board.I2C()  # uses board.SCL and board.SDA
sensor = adafruit_ahtx0.AHTx0(i2c)

while True:
    temperature = round(sensor.temperature,2)
    relative_humidity = round(sensor.relative_humidity,2)
    
    print("\nTemperature: %0.2f C" % temperature)
    print("Humidity: %0.2f %%" % relative_humidity)
    time.sleep(5)
