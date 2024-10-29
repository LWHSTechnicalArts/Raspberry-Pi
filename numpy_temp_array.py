"""
Use NumPy to create a list of temperature values created by the SHT45 sensor.
"""

import time
import board
import adafruit_sht4x
import numpy as np

# Create sensor object, communicating over the board's default I2C bus
i2c = board.I2C()  # uses board.SCL and board.SDA
sht = adafruit_sht4x.SHT4x(i2c)
print("Found SHT4x with serial number", hex(sht.serial_number))

sht.mode = adafruit_sht4x.Mode.NOHEAT_HIGHPRECISION
# Can also set the mode to enable heater
# sht.mode = adafruit_sht4x.Mode.LOWHEAT_100MS
print("Current mode is: ", adafruit_sht4x.Mode.string[sht.mode])

# Initialize an empty NumPy array to store temperature values
temperature_array = np.array([])

while True:
    temperature,relative_humidity = sht.measurements

    # Append the current temperature to the NumPy array
    temperature_array = np.append(temperature_array, round(temperature,2))
    print("\nTemperature: %0.2f C" % temperature)
    print("Humidity: %0.1f %%" % relative_humidity)
    print(temperature_array)
    
    time.sleep(5)
