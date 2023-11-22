"""
Use NumPy to create a list of temperature values created by the AHT20 sensor.
"""

import time
import board
import adafruit_ahtx0
import numpy as np

# Create sensor object, communicating over the board's default I2C bus
i2c = board.I2C()  # uses board.SCL and board.SDA
sensor = adafruit_ahtx0.AHTx0(i2c)

# Initialize an empty NumPy array to store temperature values
temperature_array = np.array([])

while True:
    temperature = round(sensor.temperature, 2)
    humidity = sensor.relative_humidity

    # Append the current temperature to the NumPy array
    temperature_array = np.append(temperature_array, temperature)

    print("\nTemperature: %0.2f C" % temperature)
    print("Humidity: %0.1f %%" % humidity)
    print(temperature_array)
    
    time.sleep(5)
