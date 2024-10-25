
# Mouse Jiggler in CircuitPython
#
# Author: Andrew Shepherd
# copyright Andrew Shepherd 2020
# Date: 2020-10-25
# Version: 1.0
# License: MIT
# 
# Description: A simple mouse jiggler to keep the computer awake.  Moves the mouse cursor slightly every 9 minutes.
# Should work on any RP2040 board with CircuitPython.  
# Tested on Adafruit QT Py RP2040 and Raspberry Pi Pico.
#
# Download CircuitPython UF2 images From:
# https://adafruit-circuit-python.s3.amazonaws.com/index.html?prefix=bin/raspberry_pi_pico/en_GB/
# https://adafruit-circuit-python.s3.amazonaws.com/index.html?prefix=bin/adafruit_qtpy_rp2040/en_GB/
# https://adafruit-circuit-python.s3.amazonaws.com/index.html?prefix=bin/sparkfun_pro_micro_rp2040/en_GB/
#
# Lib Files
# =========
# https://github.com/adafruit/Adafruit_CircuitPython_Bundle
# https://github.com/adafruit/CircuitPython_Community_Bundle
# 
# 
# REF: https://www.tomshardware.com/how-to/diy-mouse-jiggler-raspberry-pi-pico
# REF: https://learn.adafruit.com/adafruit-qt-py-2040/blink
# 

"""
__CIRCUITPYTHON_VERSION__ 9.1.4
__LIB__ Library dependencies:
adafruit_hid/
__LIB_END__
"""

from time import sleep
import board
import usb_hid
from adafruit_hid.mouse import Mouse
from digitalio import DigitalInOut, Direction
import neopixel

FEATURE_NEOPIXEL = False
FEATURE_LED_PIN = False
# LED_PIN_NUM = GPIO25
	
mouse = Mouse(usb_hid.devices)

kNineMinsInSeconds = 60 * 9

kTimeOutToPayload = kNineMinsInSeconds

def setup():
	global led
	global pixel
	global FEATURE_NEOPIXEL
	global FEATURE_LED_PIN

	if featureSupported('NEOPIXEL'):
		FEATURE_NEOPIXEL = True
		pixel = neopixel.NeoPixel(board.NEOPIXEL, 1)
	elif featureSupported('LED'):
		FEATURE_LED_PIN = True
		led = DigitalInOut(board.LED)
		led.direction = Direction.OUTPUT

def blink():
	if FEATURE_LED_PIN:
		led.value = True
		sleep(0.1)
		led.value = False
		sleep(0.9)
		
	if FEATURE_NEOPIXEL:
		pixel.fill((5, 5, 0))
		sleep(0.1)
		pixel.fill((0, 0, 0))
		sleep(0.9)

def blink_blue():
	if FEATURE_LED_PIN:
		for i in range(0, 5):
			led.value = True
			sleep(0.1)
			led.value = False
			sleep(0.1)
		
	if FEATURE_NEOPIXEL:
		for i in range(0, 5):
			pixel.fill((0, 0, 255))
			sleep(0.1)
			pixel.fill((0, 0, 0))
			sleep(0.1)

def payload_middle_click():
	mouse.click( Mouse.MIDDLE_BUTTON )
	sleep(0.1)
	mouse.click( Mouse.MIDDLE_BUTTON )

def payload_move():
	mouse.move( -10, 0 )
	sleep(0.2)
	mouse.move( 10, 0 )

def featureSupported(aFeature: str) -> bool:
	# List all available attributes in the board module
	available_features = dir(board)

	# Check if 'aFeature' is in the list of available features
	if aFeature in available_features:
		print("Feature {0} is supported.".format(aFeature) )
		return True
	else:
		print("Feature {0} is not supported.".format(aFeature) )
		return False
	
# Main entry point
def jigglerLoop() -> None:
	time_counter = kTimeOutToPayload # Execute payload immediately
	while True:

		if( time_counter >= kTimeOutToPayload):
			payload_move()
			blink_blue()
			time_counter = 0

		blink()

		time_counter += 1

#----------------------------------------------

# Main entry point
def main() -> None:
	setup()
	jigglerLoop()

#----------------------------------------------
if __name__ == "__main__":
	main()

