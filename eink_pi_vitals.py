#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
sys.path.append("/home/lick/Documents/e-Paper/RaspberryPi_JetsonNano/python/lib")
import os
picdir = "/home/lick/Documents/e-Paper/RaspberryPi_JetsonNano/python/pic"
libdir = "/home/lick/Documents/e-Paper/RaspberryPi_JetsonNano/python/lib"
import logging
from waveshare_epd import epd3in7
import time
from PIL import Image, ImageDraw, ImageFont
import traceback
from datetime import datetime
import psutil
import socket

logging.basicConfig(level=logging.DEBUG)
logging.info("Pi Stats Display")
epd = epd3in7.EPD()
logging.info("init and Clear")
epd.init(0)
epd.Clear(0xFF, 0)
font48 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 48)
font36 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 36)
font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
font20 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 20)
font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)

def get_cpu_temp():
    """Get CPU temperature"""
    try:
        with open('/sys/class/thermal/thermal_zone0/temp', 'r') as f:
            temp = float(f.read()) / 1000.0
        return f"{temp:.1f}Â°C"
    except:
        return "N/A"

def get_ip_address():
    """Get local IP address"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "No network"

def get_hostname():
    """Get hostname"""
    return socket.gethostname()

def get_stats():
    """Get Pi vital statistics"""
    stats = {
        'time': datetime.now().strftime('%H:%M'),
        'date': datetime.now().strftime('%Y-%m-%d'),
        'cpu': f"{psutil.cpu_percent()}%",
        'memory': f"{psutil.virtual_memory().percent}%",
        'disk': f"{psutil.disk_usage('/').percent}%",
        'temp': get_cpu_temp(),
        'ip': get_ip_address(),
        'hostname': get_hostname()
    }
    return stats

try:
    while True:
        logging.info("Updating display...")
        
        # Create new image
        Himage = Image.new('L', (epd.height, epd.width), 0xFF)
        draw = ImageDraw.Draw(Himage)
        
        # Get current stats
        stats = get_stats()
        
        # Draw time (large)
        draw.text((10, 10), stats['time'], font=font48, fill=0)
        
        # Draw date
        draw.text((10, 70), stats['date'], font=font20, fill=0)
        
        # Draw separator line
        draw.line((10, 100, epd.height - 10, 100), fill=0, width=2)
        
        # Draw stats with smaller font and tighter spacing
        y_pos = 115
        draw.text((10, y_pos), f"Hostname:   {stats['hostname']}", font=font20, fill=0)
        y_pos += 32
        draw.text((10, y_pos), f"IP: {stats['ip']}", font=font20, fill=0)
        y_pos += 32
        draw.text((10, y_pos), f"CPU Usage:  {stats['cpu']}", font=font20, fill=0)
        y_pos += 32
        draw.text((10, y_pos), f"Memory:     {stats['memory']}", font=font20, fill=0)
        y_pos += 32
        draw.text((10, y_pos), f"Disk:       {stats['disk']}", font=font20, fill=0)
        y_pos += 32
        draw.text((10, y_pos), f"CPU Temp:   {stats['temp']}", font=font20, fill=0)
        
        # Display on e-ink
        epd.display_4Gray(epd.getbuffer_4Gray(Himage))
        
        # Wait 30 seconds before updating
        time.sleep(30)
        
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd3in7.epdconfig.module_exit()
    exit()
