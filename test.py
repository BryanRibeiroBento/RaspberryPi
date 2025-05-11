import sys
import os
import time
import spidev
import RPi.GPIO as GPIO
from PIL import Image

# Add driver path
sys.path.append(os.path.join(os.path.dirname(__file__), 'library'))
from GC9A01 import GC9A01

# Init display
display = GC9A01(
    port=0,
    cs=0,
    dc=25,
    backlight=18,
    rst=24,
    width=240,
    height=240,
    rotation=0,
    spi_speed_hz=40000000
)

# Load and resize image
img_path = "badbunny.png"  # substitua pelo nome real da sua imagem
base_image = Image.open(img_path).convert("RGB").resize((240, 240))

# Animation loop: rotate and display
angle = 0
while True:
    rotated = base_image.rotate(angle)
    display.display(rotated)
    angle = (angle + 5) % 360
    time.sleep(0.05)