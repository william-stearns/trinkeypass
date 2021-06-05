#!/usr/bin/env python3
"""This code, designed to run on an Adafruit Neo Trinkey, sends a password
to the connected system as if it was a keyboard."""

__version__ = '0.0.16'

__author__ = 'William Stearns'
__copyright__ = 'Copyright 2021, William Stearns'
__credits__ = ['William Stearns']
__email__ = 'william.l.stearns@gmail.com'
__license__ = 'GPL 3.0'
__maintainer__ = 'William Stearns'
__status__ = 'Development'				#Prototype, Development or Production


import os
import sys
import time
#import gc
import board														# pylint: disable=import-error
import touchio														# pylint: disable=import-error
import usb_hid														# pylint: disable=import-error
import neopixel														# pylint: disable=import-error
import storage														# pylint: disable=import-error
from adafruit_hid.keyboard import Keyboard										# pylint: disable=import-error
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS								# pylint: disable=import-error
#from adafruit_hid.keycode import Keycode										# pylint: disable=import-error,unused-import


#def debug(debug_str):
#	"""Returns debugging information."""
#
#	print(debug_str)


def isdir(possible_dir):
	"""Returns whether possible_dir is a directory or not, as
	os.path.* is not currently available in micropython."""

	try:
		_ = os.listdir(possible_dir)
		return True
	except OSError:
		return False



def obj_exists(possible_object):
	"""Returns whether possible_object exists in the filesystem or
	not, as os.path.* is not currently available in micropython.
	Does not distinguish between directories and files. """

	try:
		os.stat(possible_object)
		return True
	except OSError:
		return False


def get_keypress(k1, k2):
	"""Waits for a key to be pressed, then returns which one(s) were
	pressed and the total time from first press to last release (in
	10ths of a second)."""

	t1press = False
	t2press = False
	timecycles = 0

	while (not t1press) and (not t2press):							#Keep going through the loop as loong as we've not yet seen a press
		while (k1.value ^ key_invert) or (k2.value ^ key_invert):			#While either button is pressed
			oldt1 = t1press
			oldt2 = t2press
			t1press = t1press or (k1.value ^ key_invert)
			t2press = t2press or (k2.value ^ key_invert)

			if oldt1 != t1press or oldt2 != t2press:				#If we've added a key since the last loop...
				if t1press and t2press:
					set_neo(pixels, [1, 2], color_keypress, False)		#Turn on the neopixels next to the pads.
				elif t1press:
					set_neo(pixels, [2], color_keypress, False)		#Pixel closest to pad 1
				elif t2press:
					set_neo(pixels, [1], color_keypress, False)		#Pixel closest to pad 2
			time.sleep(0.1)
			timecycles += 1

	set_neo(pixels, default_pixels, default_color, True)

	return t1press, t2press, timecycles


def load_file_into_string(filename):
	"""Reads the entire contents of a file into the returned string.  First returned object is string form, second is raw bytes."""

	file_string = None
	raw_bytes = None

	if obj_exists(filename) and not isdir(filename):				#Can't use python's "os.path.exists"
		#print("Reading " +str(filename))
		#try:
		with open(filename, 'rb') as read_h:
			raw_bytes = read_h.read()
			#file_string = raw_bytes.decode('utf-8', "replace")
			file_string = str(raw_bytes, 'ascii')

		#except PermissionError:
		#except:
		#	pass

	return file_string, raw_bytes


def load_raw_keyfile(passfile_dir, key_filename):
	"""Load the contents of the requested key."""

	content = None

	filename = passfile_dir + key_filename
	if obj_exists(filename) and not isdir(filename):
		content, _ = load_file_into_string(filename)
	else:
		print("Unable to locate " + filename)

	return content


#def transform_raw(raw_string, xform_key):
#	"""Converts a raw string into a transformed string."""
#	#If xform_key empty or false, just return the string as is.
#	#If xform_key non-empty, swap the case of all keys lining up with Trues in xform_key (we can think of xform_key being repeated over and over enough to cover the entire raw_string.
#
#	if xform_key:
#		output_text = ''
#		for s_index, orig_char in enumerate(raw_string):
#			#Loop through the xform key values, wrapping around to the 0th element when we get to the end.
#			if xform_key[s_index % len(xform_key)]:						#Pull out the True/False value from xform_key
#				if orig_char.isupper():
#					output_text = output_text + orig_char.lower()
#				elif orig_char.isdigit():
#					output_text = output_text + str(9 - int(orig_char))	#Replace each digit with 9-thatdigit
#				else:
#					output_text = output_text + orig_char.upper()
#			else:
#				output_text = output_text + orig_char
#	else:
#		output_text = raw_string
#
#	return output_text


def flash_neo(pixel_h, which_ones, color, how_long):
	"""Flash all neopixels in the which_ones list to a given color for the given time."""

	for pix in which_ones:
		pixel_h[pix] = color
		pixel_h.brightness = neo_brightness
		pixel_h.show()
	time.sleep(how_long)
	set_neo(pixel_h, default_pixels, default_color, True)


def set_neo(pixel_h, which_ones, color, clean_slate):
	"""Set all neopixels in the which_ones list to a given color."""

	for pix in range(0, 4):
		if pix in which_ones:
			pixel_h[pix] = color
		elif clean_slate:
			pixel_h[pix] = color_blank
	pixel_h.brightness = neo_brightness
	pixel_h.show()





#Constants
num_to_neo = [ [], [0], [1], [0,1], [2], [0,2], [1,2], [0,1,2], [3], [0,3], [1,3], [0,1,3], [2,3], [0,2,3], [1,2,3], [0,1,2,3] ]	#For a number 0-15, which neopixels do we light to show it?
red = (32, 0, 0)
green = (0, 32, 0)
blue = (0, 0, 32)
cyan = (0, 32, 32)
purple = (32, 0, 32)
yellow = (32, 32, 0)
white = (32, 32, 32)
black = (0, 0, 0)
zero_pads = '0000'

#User-editable values
seconds_to_erase = 7
max_unlock_failures = 7
neo_brightness = 0.2

color_keynum = green
color_wakeup = blue
color_keypress = purple
color_blank = black
#color_xform_mode = cyan
color_unlock_mode = yellow
color_error = red


#Setup
if os.uname().machine == 'Adafruit NeoPixel Trinkey M0 with samd21e18':
	key_invert = False

	pixels = neopixel.NeoPixel(board.NEOPIXEL, 4, brightness=neo_brightness, auto_write=False)

	keyboard = Keyboard(usb_hid.devices)
	keyboard_layout = KeyboardLayoutUS(keyboard)

	touch1 = touchio.TouchIn(board.TOUCH1)
	touch2 = touchio.TouchIn(board.TOUCH2)
else:
	print("I don't know how to run on this platform: " + os.uname().machine)
	print("Here are its hardware features: " + str(dir(board)))
	sys.exit(1)

selected_keynum = 0
#xform_entry_mode = False
unlock_entry_mode = False
#xform_list = []
unlock_code = ""
unlock_failures = 0
default_color = color_keynum

#try:
#	from secrets import secrets
#except ImportError:
#	secrets = {}
#
#if 'unlock' not in secrets:
#	secrets['unlock'] = ''



if obj_exists('/sd/') and isdir('/sd/'):					#Where will the password files be?
	data_dir = '/sd/'							#If this circuitpython board has a microsd slot, the contents of this will show up under /sd/
else:
	data_dir = '/'								#Otherwise, the contents will be immediately at the top of the filesystem.

pw_subdir = ''									#This dir is under data_dir, equal to unlock_code (unless the directory does not exist, then empty so we use the password files in data_dir)

default_pixels = []

for led in [0, 1, 2, 3]:
	flash_neo(pixels, [led], color_wakeup, 1)

while True:
	#print(str(gc.mem_free()) + " bytes free")				# pylint: disable=no-member
	(t1, t2, cycles) = get_keypress(touch1, touch2)
	#print(str(t1) + ' ' + str(t2) + ' ' + str(cycles))
	if t1 and t2:
		#Both Touch1 and Touch2 pressed.  This switches back and forth between normal (select/send keys) mode and enter xform mode.
		if cycles >= (seconds_to_erase * 10):
			#Erasing the entire storage because the user held both keys for more than 7 seconds
			storage.erase_filesystem()
		#if xform_entry_mode:
		#	#Switching back to normal operation
		#	default_color = color_keynum
		#	default_pixels = num_to_neo[selected_keynum % 16]
		#	set_neo(pixels, default_pixels, default_color, True)
		elif unlock_entry_mode:
			#Switching back to normal operation
			default_color = color_keynum
			default_pixels = num_to_neo[selected_keynum % 16]
			if not obj_exists(data_dir + unlock_code) or not isdir(data_dir + unlock_code):
				#Supplied unlock_code does not correspond to a dir in the filesystem; track how many fails and erase_filesystem if too many
				unlock_failures += 1
				if unlock_failures > max_unlock_failures:
					#Erasing the entire storage because there were more than 7 unlock failures
					storage.erase_filesystem()
			elif obj_exists(data_dir + unlock_code) and isdir(data_dir + unlock_code):		# and obj_exists(data_dir + unlock_code + '/0000.txt'):
				pw_subdir = unlock_code + '/'
				selected_keynum = 0
				default_pixels = num_to_neo[selected_keynum % 16]
				if unlock_code:
					#You only reset the failure count if you actually guess a correct one, not by going back to the top level directory with an empty unlock code.
					unlock_failures = 0
		else:
			#Switching into unlock entry mode
			default_color = color_unlock_mode
			default_pixels = [0,3]
			unlock_code = ""

		set_neo(pixels, default_pixels, default_color, True)
		unlock_entry_mode = unlock_entry_mode ^ True			#xor with true to switch to opposite value (True->False, False->True)

	elif t1:
		#Only T1 pressed.  In normal mode, this moves us to the next password.  In "enter xform" mode, add a "False/nocasechange" to the xform list.
		#if xform_entry_mode:
		#	xform_list.append(False)
		#	print(str(xform_list))
		if unlock_entry_mode:
			unlock_code = unlock_code + '1'
		#elif unlock_code != secrets['unlock']:
		#	flash_neo(pixels, [0, 3], color_unlock_mode, 0.5)
		else:
			if selected_keynum == 9999:
				selected_keynum = 0
			elif obj_exists(data_dir + pw_subdir + (zero_pads + str(selected_keynum + 1))[-4:] + '.txt'):
				selected_keynum += 1
			else:
				selected_keynum = 0

			default_pixels = num_to_neo[selected_keynum % 16]
			set_neo(pixels, default_pixels, color_keynum, True)

	elif t2:
		#Only T2 pressed.  In normal mode, send the currently selected password like a keyboard.  In "enter xform" mode, add a "True/casechange" to the xform list.
		#if xform_entry_mode:
		#	xform_list.append(True)
		#	print(str(xform_list))
		if unlock_entry_mode:
			unlock_code = unlock_code + '2'
		#elif unlock_code != secrets['unlock']:
		#	flash_neo(pixels, [0, 3], color_unlock_mode, 0.5)
		else:
			#target_string = transform_raw(load_raw_keyfile(data_dir + pw_subdir, (zero_pads + str(selected_keynum))[-4:] + '.txt'), xform_list)
			target_string = load_raw_keyfile(data_dir + pw_subdir, (zero_pads + str(selected_keynum))[-4:] + '.txt')
			if target_string:
				keyboard_layout.write(target_string)
