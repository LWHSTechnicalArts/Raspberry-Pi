# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
Basic `SHT45` example test with Matplotlib
"""

import time
import board
import adafruit_sht4x
import numpy as np
import matplotlib.pyplot as plt

# Create sensor object, communicating over the board's default I2C bus
i2c = board.I2C()  # uses board.SCL and board.SDA
sensor = adafruit_sht4x.SHT4x(i2c)
sensor.mode = adafruit_sht4x.Mode.NOHEAT_HIGHPRECISION  # Set the SHT45 mode

# Initialize an empty NumPy array to store temperature values
temperature_array = np.array([])

# Initialize time array for x-axis of the plot
time_array = np.array([])

# Create a figure and axis for the plot
fig, ax = plt.subplots()

# Initialize a counter for time in seconds
time_counter = 0

while True:
    temperature, humidity = sensor.measurements  # Read temperature and humidity from SHT45
    temperature = round(temperature, 2)

    # Append the current temperature to the NumPy array
    temperature_array = np.append(temperature_array, temperature)

    # Append the current time (in seconds) to the time array
    time_array = np.append(time_array, time_counter)

    print("\nTemperature: %0.2f C" % temperature)
    print("Humidity: %0.1f %%" % humidity)

    # Plot the temperature values over time
    ax.plot(time_array, temperature_array, label='Temperature (C)')

    # Add labels and title to the plot
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Temperature (C)')
    ax.set_title('Temperature over Time')

    # Display legend
    ax.legend()

    # Pause to allow the plot to update
    plt.pause(2)

    # Increment the time counter
    time_counter += 2

    # Clear the plot for the next iteration
    ax.clear()
