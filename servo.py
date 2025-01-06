"""Simple test for a continuous rotation servo on channel 15 and a standard servo on 14."""
import time
from adafruit_servokit import ServoKit
 
# Set channels to the number of servo channels on your kit.
# 8 for FeatherWing, 16 for Shield/HAT/Bonnet.
kit = ServoKit(channels=16)

while True: 
    kit.servo[1].angle = 180
    kit.continuous_servo[0].throttle = 1
    time.sleep(2)
    kit.continuous_servo[0].throttle = -1
    time.sleep(2)
    kit.servo[1].angle = 0
    kit.continuous_servo[0].throttle = 0.08    #change this number to find stop value
    time.sleep(5)
