from gpiozero import Button
from signal import pause
import time

# Define button on GPIO pin 19
button = Button(19)

print('start')

# Function to call when button is pressed
def on_button_press():
    print('Button Pressed')
    time.sleep(0.2)  # debounce delay

# Attach the function to the button press event
button.when_pressed = on_button_press

# Keep the program running to listen for button presses
pause()
