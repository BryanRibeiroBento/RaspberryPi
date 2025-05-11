import sys
import os
import time
import spidev
import RPi.GPIO as GPIO
from PIL import Image,ImageDraw,ImageFont
sys.path.append(os.path.join(os.path.dirname(__file__),'library'))
from GC9A01 import GC9A01

display = GC9A01(
	port = 0,
	cs = 0,
	dc = 25,
	backlight = 18,
	rst = 24,
	width = 240,
	height = 240,
	rotation = 0,
	spi_speed_hz = 40000000
	
)


test = 12

image = Image.new("RGB",(240,240),(15,32,128))
draw = ImageDraw.Draw(image)

font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",20)
text = "Testing if it works"

w,h = draw.textsize(text, font = font)
x = (240-w)//2
y = (240-h) //2
draw.text((x,y),text,font = font,fill=(255,255,255))


display.display(image)

time.sleep(10)
