import time
import board
import adafruit_vl53l1x
import numpy as np
import matplotlib.pyplot as plt

# Create sensor object, communicating over the board's default I2C bus
i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller

vl53 = adafruit_vl53l1x.VL53L1X(i2c)

# OPTIONAL: can set non-default values
vl53.distance_mode = 1
vl53.timing_budget = 100

print("VL53L1X Simple Test.")
print("--------------------")
model_id, module_type, mask_rev = vl53.model_info
print("Model ID: 0x{:0X}".format(model_id))
print("Module Type: 0x{:0X}".format(module_type))
print("Mask Revision: 0x{:0X}".format(mask_rev))
print("Distance Mode: ", end="")
if vl53.distance_mode == 1:
    print("SHORT")
elif vl53.distance_mode == 2:
    print("LONG")
else:
    print("UNKNOWN")
print("Timing Budget: {}".format(vl53.timing_budget))
print("--------------------")

vl53.start_ranging()

# Initialize an empty NumPy array to store temperature values
distance_array = np.array([])

# Initialize time array for x-axis of the plot
time_array = np.array([])

# Create a figure and axis for the plot
fig, ax = plt.subplots()

# Initialize a counter for time in seconds
time_counter = 0

while True:
    if vl53.data_ready:
        print("Distance: {} cm".format(vl53.distance))
        vl53.clear_interrupt()
        

    # Append the current temperature to the NumPy array
    if vl53.distance is not None:
        distance_array = np.append(distance_array, vl53.distance)
        print(distance_array)
        #Append the current time (in seconds) to the time array
        time_array = np.append(time_array, time_counter)

 
    # Plot the temperature values over time
    ax.plot(time_array, distance_array, label='Distance (cm)')

    # Add labels and title to the plot
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Distance (cm)')
    ax.set_title('Distance over Time')

    # Display legend
    ax.legend()

    # Pause to allow the plot to update
    plt.pause(2)

    # Increment the time counter
    time_counter += 2

    # Clear the plot for the next iteration
    ax.clear()

