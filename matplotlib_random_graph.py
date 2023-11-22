import matplotlib.pyplot as plt
import random
from itertools import count
from matplotlib.animation import FuncAnimation

# Initialize an empty list to store the data
x_data = []
y_data = []

# Create a function to generate random data
def generate_data():
    x_data.append(next(x))
    y_data.append(random.randint(0, 100))

# Create a counter to generate x-values
x = count()

# Create a function to update the plot
def update_plot(i):
    generate_data()
    plt.cla()  # Clear the current plot
    plt.plot(x_data, y_data, label='Random Data - cntl+w to quit')
    plt.legend()
    plt.xlabel('Time')
    plt.ylabel('RandNumber')
    plt.title('Live Matplotlib Graph')

# Create a Matplotlib animation
ani = FuncAnimation(plt.gcf(), update_plot, interval=1000)  # Update every 1 second (1000 ms)
mng = plt.get_current_fig_manager()
mng.full_screen_toggle()
plt.show()
