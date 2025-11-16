import time
import board
import adafruit_vl53l1x
import numpy as np
import matplotlib.pyplot as plt

# Create sensor object
i2c = board.I2C()
vl53 = adafruit_vl53l1x.VL53L1X(i2c)

# Configure sensor
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

# Use lists for better performance (convert to numpy later if needed)
distance_list = []
time_list = []

# Create interactive plot
plt.ion()  # Turn on interactive mode
fig, ax = plt.subplots()
line, = ax.plot([], [], 'b-', label='Distance (cm)')
ax.set_xlabel('Time (s)')
ax.set_ylabel('Distance (cm)')
ax.set_title('Distance over Time')
ax.legend()
ax.grid(True)

start_time = time.time()

try:
    while True:
        if vl53.data_ready:
            distance = vl53.distance
            current_time = time.time() - start_time
            
            print("Distance: {} cm at {:.2f}s".format(distance, current_time))
            
            # Append to lists
            distance_list.append(distance)
            time_list.append(current_time)
            
            # Update plot data
            line.set_data(time_list, distance_list)
            
            # Auto-scale axes
            ax.relim()
            ax.autoscale_view()
            
            # Redraw
            fig.canvas.draw()
            fig.canvas.flush_events()
            
            vl53.clear_interrupt()
        
        time.sleep(0.1)  # Small delay to prevent CPU spinning

except KeyboardInterrupt:
    print("\nStopping measurement...")
    vl53.stop_ranging()
    plt.ioff()
    plt.show()  # Keep the final plot open
