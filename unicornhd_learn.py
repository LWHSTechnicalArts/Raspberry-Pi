import time
import unicornhathd

uh = unicornhathd
uh.brightness(0.5)
uh.rotation(0)

uh.set_pixel(10, 10, 255, 255, 0)   #set one pixel
uh.show()

time.sleep(3)

for x in range(16):                      #loop to set all pixels
    for y in range(16):
        uh.set_pixel(x, y, 0, 255, 255)
uh.show()

time.sleep(10)

uh.clear()           #clear all pixels
uh.show()
