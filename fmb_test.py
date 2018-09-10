import tweepy
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

consumer_key = '49flQYZIFgw2w3Jshycwgv1di'
consumer_secret = 'ZrVb1qFuZ8MroSAVvf4WyubMm2sue7pTCpC87wiPVre4unfYPd'
access_token = '2280220887-65z66kQjlL9AelcELOmq5FKQdhcsVB05lN9Up8s'
access_token_secret = 'l5yeE3VyIKZRVLXxjf9mMh8WvRCUj7tuUqp5w6KaiepCl'

def is_ascii(s):
	return all(ord(c) < 128 for c in s)

#override tweepy.StreamListener to add logic to on_status
class MyStreamListener(tweepy.StreamListener):
	def __init__(self, user):
		super().__init__()
		self.user = user
		self.scroll_worker = ScrollWorker()
		self.daemon = True
		self.scroll_worker.start()

	def on_status(self, status):
		if not self.scroll_worker.is_busy:
			if is_ascii(status.text):
				self.scroll_worker.current_message = status.text
				print(status)
			else:
				print('*** IGNORED (NON-ASCII) ***', status.text)
		else:
			print('*** IGNORED *** ', status.text)

	def on_error(self, status_code):
		print('error: ', status_code)

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
				show_message(self.device, self.current_message, fill="white", font=proportional(LCD_FONT), scroll_delay=0.02)
				time.sleep(1)
				self.current_message = None
				self.is_busy = False

	def _stop(self):
		self.device.cleanup()
		super()._stop()

def main():
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	api = tweepy.API(auth)

	user = api.get_user('realDonaldTrump')

	myStreamListener = MyStreamListener(user)

	myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)
	myStream.filter(follow=[user.id_str], async=True)
	#myStream.filter(track=['#HarryPotter','#ReplaceAMovieTitleWithFanny'], async=True)

if __name__ == "__main__":
    # execute only if run as a script
    main()