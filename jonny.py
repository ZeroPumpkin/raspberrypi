from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.virtual import viewport
from PIL import ImageFont
import time

serial = spi(port=0, device=0, gpio=noop())
device = max7219(serial, cascaded=4, block_orientation=-90, rotate=0)
device.contrast(0x09)

fnt = ImageFont.truetype('/home/pi/Downloads/pixelmix.ttf', 6)
fnt8 = ImageFont.truetype('/home/pi/Downloads/pixelmix.ttf', 8)

x = device.width

virtual = viewport(device, width=500, height=device.height)

with canvas(virtual) as draw:
    draw.rectangle((x + 0, 0, x + 7, 7), fill="white")
    draw.rectangle((x + 9, 0, x + 16, 7), fill="white")
    draw.rectangle((x + 18, 0, x + 25, 7), fill="white")
    draw.text((x + 2, 1), "B", font=fnt, fill=None)
    draw.text((x + 11, 1), "B", font=fnt, fill=None)
    draw.text((x + 20, 1), "C", font=fnt, fill=None)
    draw.text((x + 30, 0), "BREAKING NEWS: JONNY'S A LOSER", font=fnt8, fill="white")

while True:
    for x in range(300):
        virtual.set_position((x, 0))
        time.sleep(0.04)
