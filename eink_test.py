#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
sys.path.append("/home/pi/Documents/e-Paper/RaspberryPi_JetsonNano/python/lib")
import os
picdir = "/home/pi/Documents/e-Paper/RaspberryPi_JetsonNano/python/pic"
libdir = "/home/pi/Documents/e-Paper/RaspberryPi_JetsonNano/python/lib"
import logging
from waveshare_epd import epd3in7
import time
from PIL import Image,ImageDraw,ImageFont
import traceback

logging.basicConfig(level=logging.DEBUG)

logging.info("Demo")
        
epd = epd3in7.EPD()
logging.info("init and Clear")
epd.init(0)
epd.Clear(0xFF, 0)

font48 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 48)
font36 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 36)
font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)


while True:
    try:
        logging.info("1.Drawing on the image...")
        Himage = Image.new('L', (epd.height, epd.width), 0xFF)  # 0xFF: clear the frame
        draw = ImageDraw.Draw(Himage)
        draw.text((10, 10), 'hello squirrel', font = font48, fill = 0)
        epd.display_4Gray(epd.getbuffer_4Gray(Himage))
        
        time.sleep(5)
        
        Himage = Image.new('L', (epd.height, epd.width), 0x00)  # 0xFF: clear the frame
        draw = ImageDraw.Draw(Himage)
        draw.text((10, 100), 'hello squirrel', font = font48, fill = 255)
        epd.display_4Gray(epd.getbuffer_4Gray(Himage))
        
        time.sleep(5)
        
    except IOError as e:
        logging.info(e)
        
    except KeyboardInterrupt:    
        logging.info("ctrl + c:")
        epd3in7.epdconfig.module_exit()
        exit()
