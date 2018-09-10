from threading import Thread
import time

import re
import time
import argparse

from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.virtual import viewport
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, CP437_FONT, TINY_FONT, SINCLAIR_FONT, LCD_FONT

import zanelowe

def is_ascii(s):
	return all(ord(c) < 128 for c in s)

class ScrollWorker(Thread):
	def __init__(self):
		super().__init__()
		self.is_busy = False
		self.current_message = None
		# create matrix device
		self.serial = spi(port=0, device=0, gpio=noop())
		self.device = max7219(self.serial, cascaded=4, block_orientation=-90, rotate=0)
		self.device.contrast(0x09)
		print("Created device")

	def run(self):
		while True:
			if self.current_message != None:
				self.is_busy = True
				print(self.current_message)
				show_message(self.device, self.current_message, fill="white", font=proportional(LCD_FONT), scroll_delay=0.05)
				time.sleep(1)
				self.current_message = None
				self.is_busy = False

	def _stop(self):
		self.device.cleanup()
		super()._stop()

def main():
	scroll_worker = ScrollWorker()
	scroll_worker.start()

	while True:
		text = zanelowe.get_text()
		scroll_worker.current_message = text
		time.sleep(300)

if __name__ == "__main__":
    # execute only if run as a script
    main()