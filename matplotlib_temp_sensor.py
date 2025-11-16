import time
import board
import adafruit_sht4x
import matplotlib.pyplot as plt

# Create sensor object
i2c = board.I2C()
sensor = adafruit_sht4x.SHT4x(i2c)
sensor.mode = adafruit_sht4x.Mode.NOHEAT_HIGHPRECISION

# Use lists for better performance
temperature_list = []
humidity_list = []
time_list = []

# Create interactive plot with two subplots
plt.ion()  # Turn on interactive mode
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

# Initialize line objects
temp_line, = ax1.plot([], [], 'r-', label='Temperature (Â°C)', linewidth=2)
humid_line, = ax2.plot([], [], 'b-', label='Humidity (%)', linewidth=2)

# Configure temperature plot
ax1.set_xlabel('Time (s)')
ax1.set_ylabel('Temperature (Â°C)')
ax1.set_title('Temperature over Time')
ax1.legend()
ax1.grid(True, alpha=0.3)

# Configure humidity plot
ax2.set_xlabel('Time (s)')
ax2.set_ylabel('Humidity (%)')
ax2.set_title('Humidity over Time')
ax2.legend()
ax2.grid(True, alpha=0.3)

plt.tight_layout()

start_time = time.time()
SAMPLE_INTERVAL = 2  # seconds between readings

try:
    while True:
        # Read sensor
        temperature, humidity = sensor.measurements
        current_time = time.time() - start_time
        
        # Store data
        temperature_list.append(round(temperature, 2))
        humidity_list.append(round(humidity, 1))
        time_list.append(current_time)
        
        # Print to console
        print("\nTime: {:.1f}s".format(current_time))
        print("Temperature: {:.2f} Â°C".format(temperature))
        print("Humidity: {:.1f} %".format(humidity))
        
        # Update temperature plot
        temp_line.set_data(time_list, temperature_list)
        ax1.relim()
        ax1.autoscale_view()
        
        # Update humidity plot
        humid_line.set_data(time_list, humidity_list)
        ax2.relim()
        ax2.autoscale_view()
        
        # Redraw
        fig.canvas.draw()
        fig.canvas.flush_events()
        
        time.sleep(SAMPLE_INTERVAL)

except KeyboardInterrupt:
    print("\n\nStopping measurement...")
    print("Final statistics:")
    print("  Avg Temperature: {:.2f} Â°C".format(sum(temperature_list) / len(temperature_list)))
    print("  Min Temperature: {:.2f} Â°C".format(min(temperature_list)))
    print("  Max Temperature: {:.2f} Â°C".format(max(temperature_list)))
    print("  Avg Humidity: {:.1f} %".format(sum(humidity_list) / len(humidity_list)))
    print("  Min Humidity: {:.1f} %".format(min(humidity_list)))
    print("  Max Humidity: {:.1f} %".format(max(humidity_list)))
    
    plt.ioff()
    plt.show()  # Keep the final plot open
