from flask import Flask, render_template
import RPi.GPIO as GPIO

app = Flask(__name__)

# Set up GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
led_pin = 18  # Change this to the GPIO pin you connected the LED to
GPIO.setup(led_pin, GPIO.OUT)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/turn_on')
def turn_on():
    GPIO.output(led_pin, GPIO.HIGH)
    return 'LED turned on'

@app.route('/turn_off')
def turn_off():
    GPIO.output(led_pin, GPIO.LOW)
    return 'LED turned off'

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)

