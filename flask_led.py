from flask import Flask, render_template
from gpiozero import LED
import time
led = LED(18)

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/turn_on')
def turn_on():
    led.on()
    return 'LED turned on'

@app.route('/turn_off')
def turn_off():
    led.off()
    return 'LED turned off'

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)
