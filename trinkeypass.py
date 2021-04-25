#!/usr/bin/env python3
"""This code, designed to run on an Adafruit Neo Trinkey, sends a password
to the connected system as if it was a keyboard."""

__version__ = '0.0.9'

__author__ = 'William Stearns'
__copyright__ = 'Copyright 2021, William Stearns'
__credits__ = ['William Stearns']
__email__ = 'william.l.stearns@gmail.com'
__license__ = 'GPL 3.0'
__maintainer__ = 'William Stearns'
__status__ = 'Development'				#Prototype, Development or Production


import os
import time
import board														# pylint: disable=import-error
import touchio														# pylint: disable=import-error
import usb_hid														# pylint: disable=import-error
import neopixel														# pylint: disable=import-error
from adafruit_hid.keyboard import Keyboard										# pylint: disable=import-error
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS								# pylint: disable=import-error
#from adafruit_hid.keycode import Keycode										# pylint: disable=import-error,unused-import



def debug(debug_str):
	"""Returns debugging information."""

	print(debug_str)


def isdir(possible_dir):
	"""Returns whether possible_dir is a directory or not, as
	os.path.* is not currently available in micropython."""

	isdir_return = False
	try:
		_ = os.listdir(possible_dir)
		isdir_return = True
	except OSError:
		pass

	return isdir_return


def obj_exists(possible_object):
	"""Returns whether possible_object exists in the filesystem or
	not, as os.path.* is not currently available in micropython.
	Does not distinguish between directories and files. """

	obj_exists_return = False
	try:
		os.stat(possible_object)
		obj_exists_return = True
	except OSError:
		pass

	return obj_exists_return


def hid_inject_string(target_string):
	"""Passes along the given string to the connected system as if
	 this was a keyboard."""

	if target_string:
		keyboard_layout.write(target_string)
	else:
		debug("Empty string detected, not writing")


def get_keypress(k1, k2):
	"""Waits for a key to be pressed, then returns which one(s) were
	pressed and the total time from first press to last release (in
	10ths of a second)."""

	t1press = False
	t2press = False
	timecycles = 0

	while (not t1press) and (not t2press):
		if k1.value or k2.value:
			oldt1 = t1press
			oldt2 = t2press
			t1press = t1press or k1.value
			t2press = t2press or k2.value

			if oldt1 != t1press or oldt2 != t2press:				#If we've added a key since the last loop...
				if t1press and t2press:
					set_neo(pixels, [1, 2], color_keypress, False)		#Turn on the neopixels next to the pads.
				elif t1press:
					set_neo(pixels, [2], color_keypress, False)		#Pixel closest to pad 1
				elif t2press:
					set_neo(pixels, [1], color_keypress, False)		#Pixel closest to pad 2

			while k1.value or k2.value:
				time.sleep(0.1)
				timecycles += 1
		else:
			time.sleep(0.1)

	set_neo(pixels, default_pixels, default_color, True)

	return t1press, t2press, timecycles


def load_file_into_string(filename):
	"""Reads the entire contents of a file into the returned string.  First returned object is string form, second is raw bytes."""

	file_string = None
	raw_bytes = None

	if obj_exists(filename) and not isdir(filename):				#Can't use python's "os.path.exists"
		#debug("Reading " +str(filename))
		#try:
		with open(filename, 'rb') as read_h:
			raw_bytes = read_h.read()
			#file_string = raw_bytes.decode('utf-8', "replace")
			file_string = str(raw_bytes, 'ascii')

		#except PermissionError:
		#except:
		#	pass

	return file_string, raw_bytes


def pad_zeroes(in_num):
	"""Prepend 0's so we have a 4 digit number."""

	out_str = str(in_num)
	while len(out_str) < 4:
		out_str = '0' + out_str

	return out_str


def load_raw_keyfile(passfile_dir, padded_key_number):
	"""Load the contents of the requested key."""

	content = None

	filename = passfile_dir + padded_key_number + '.txt'
	if obj_exists(filename) and not isdir(filename):
		content, _ = load_file_into_string(filename)
	else:
		debug("Unable to locate " + filename)

	return content


#def delete_files(passfile_dir):
#	"""Deletes all password files from this device."""
#
#	for passnum in range(0, 10000):
#		filename = passfile_dir + pad_zeroes(passnum) + '.txt'
#		if obj_exists(filename) and not isdir(filename):
#			os.remove(filename)


def transform_raw(raw_string, xform_key):
	"""Converts a raw string into a transformed string."""
	#If xform_key empty or false, just return the string as is.
	#If xform_key non-empty, swap the case of all keys lining up with Trues in xform_key (we can think of xform_key being repeated over and over enough to cover the entire raw_string.

	if xform_key:
		output_text = ''
		for s_index in range(0, len(raw_string)):
			#Loop through the xform key values, wrapping around to the 0th element when we get to the end.
			if xform_key[s_index % len(xform_key)]:						#Pull out the True/False value from xform_key
				if raw_string[s_index].isupper():
					output_text = output_text + raw_string[s_index].lower()
				elif raw_string[s_index].isdigit():
					output_text = output_text + str(9 - int(raw_string[s_index]))	#Replace each digit with 9-thatdigit
				else:
					output_text = output_text + raw_string[s_index].upper()
			else:
				output_text = output_text + raw_string[s_index]
	else:
		output_text = raw_string

	return output_text


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


def show_num(pixel_h, number, color):
	"""Show binary of the given number in that color."""

	show_number = number % 16

	which_pixels = []

	if show_number >= 8:
		which_pixels.insert(0, 3)
		show_number -= 8

	if show_number >= 4:
		which_pixels.insert(0, 2)
		show_number -= 4

	if show_number >= 2:
		which_pixels.insert(0, 1)
		show_number -= 2

	if show_number >= 1:
		which_pixels.insert(0, 0)

	set_neo(pixel_h, which_pixels, color, True)

	return which_pixels


#Constants
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
cyan = (0, 255, 255)
purple = (255, 0, 255)
yellow = (255, 255, 0)
white = (255, 255, 255)
black = (0, 0, 0)


#User-editable values
seconds_to_erase = 7
neo_brightness = 0.2

color_keynum = green
color_wakeup = blue
color_keypress = purple
color_blank = black
color_xform_mode = cyan
color_error = red


#Setup
pixels = neopixel.NeoPixel(board.NEOPIXEL, 4, brightness=neo_brightness, auto_write=False)

keyboard = Keyboard(usb_hid.devices)
keyboard_layout = KeyboardLayoutUS(keyboard)

touch1 = touchio.TouchIn(board.TOUCH1)
touch2 = touchio.TouchIn(board.TOUCH2)

selected_keynum = 0
xform_entry_mode = False
xform_list = []
default_color = color_keynum


if obj_exists('/sd/') and isdir('/sd/'):					#Where will the password files be?
	data_dir = '/sd/'							#If this circuitpython board has a microsd slot, the contents of this will show up under /sd/
else:
	data_dir = '/'								#Otherwise, the contents will be immediately at the top of the filesystem.

default_pixels = []

flash_neo(pixels, [0], color_wakeup, 1)
flash_neo(pixels, [1], color_wakeup, 1)
flash_neo(pixels, [2], color_wakeup, 1)
flash_neo(pixels, [3], color_wakeup, 1)

while True:
	(t1, t2, cycles) = get_keypress(touch1, touch2)
	#debug(str(t1) + ' ' + str(t2) + ' ' + str(cycles))
	if t1 and t2:
		#Both Touch1 and Touch2 pressed.  This switches back and forth between normal (select/send keys) mode and enter xform mode.
		#if cycles < (seconds_to_erase * 10):
		if xform_entry_mode:
			#debug("Switching back to normal operation")
			default_color = color_keynum
			default_pixels = show_num(pixels, selected_keynum, default_color)
		else:
			#debug("Switching into xform entry mode")
			default_color = color_xform_mode
			default_pixels = [3]
			set_neo(pixels, default_pixels, default_color, True)
			xform_list = []

		xform_entry_mode = xform_entry_mode ^ True			#xor with true to switch to opposite value (True->False, False->True)
		#Note: this program can't delete files while the storage is mounted by the host.  Disable feature for the moment.
		#else:
		#	debug("Erasing now\n")
		#	delete_files(data_dir)

	elif t1:
		#Only T1 pressed.  In normal mode, this moves us to the next password.  In "enter xform" mode, add a "False/nocasechange" to the xform list.
		if xform_entry_mode:
			xform_list.append(False)
			debug(str(xform_list))
		else:
			if selected_keynum == 9999:
				selected_keynum = 0
			elif obj_exists(data_dir + pad_zeroes(selected_keynum + 1) + '.txt'):
				selected_keynum += 1
			else:
				selected_keynum = 0

			default_pixels = show_num(pixels, selected_keynum, color_keynum)


	elif t2:
		#Only T2 pressed.  In normal mode, send the currently selected password like a keyboard.  In "enter xform" mode, add a "True/casechange" to the xform list.
		if xform_entry_mode:
			xform_list.append(True)
			debug(str(xform_list))
		else:
			hid_inject_string(transform_raw(load_raw_keyfile(data_dir, pad_zeroes(selected_keynum)), xform_list))
