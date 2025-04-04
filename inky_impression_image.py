#!/usr/bin/env python3

import sys
from PIL import Image
from inky.auto import auto

# Trick auto() into using hardcoded display settings
# This simulates passing CLI args to the script
sys.argv = [
    "inkytest2.py",          # Fake script name
    "--type", "impressions",  # Try "impressions" or "impression" depending on lib version
    "--colour", "7color"
]

# Now auto() will succeed without hardware detection
inky = auto(ask_user=False, verbose=True)

# Hardcoded image path and settings
image_path = "/home/lick/Documents/images/superman.png"
saturation = 1.0

# Get display resolution (width, height)
width, height = inky.resolution

# Load and resize the image
img = Image.open(image_path)
# Rotate first
rotated = img.rotate(90, expand=True)  # Use expand=True to keep full image size

# Now resize to match display resolution
# BUT first, match the orientation before resizing
if rotated.width != width or rotated.height != height:
    rotated = rotated.resize((width, height))

# Send to display
inky.set_image(rotated)
inky.show()
