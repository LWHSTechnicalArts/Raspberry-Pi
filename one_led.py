from gpiozero import LED
import time
led = LED(18)

while True:
    led.on()
    print("Into the light")
    time.sleep(0.5)
    led.off()
    print("The darkness is here")
    time.sleep(0.5)
