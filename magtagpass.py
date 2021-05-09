#!/usr/bin/env python3
"""This code, designed to run on an Adafruit Magtag, sends a password
to the connected system as if it was a keyboard."""

__version__ = '0.0.18'

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
import usb_hid														# pylint: disable=import-error
from adafruit_hid.keyboard import Keyboard										# pylint: disable=import-error
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS								# pylint: disable=import-error
from adafruit_bitmap_font import bitmap_font										# pylint: disable=import-error
from adafruit_display_shapes.line import Line										# pylint: disable=import-error
from adafruit_display_text import label											# pylint: disable=import-error
#import storage														# pylint: disable=import-error


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


def get_keypress(k1, k2, k3, k4):
	"""Waits for a key to be pressed, then returns which one(s) were
	pressed and the total time from first press to last release (in
	10ths of a second)."""

	global refresh_needed

	t1press = False
	t2press = False
	t3press = False
	t4press = False
	timecycles = 0

	while (not t1press) and (not t2press) and (not t3press) and (not t4press):		#Keep going through the loop as long as we've not yet seen a press
		while (k1.value ^ key_invert) or (k2.value ^ key_invert) or (k3.value ^ key_invert) or (k4.value ^ key_invert):
			oldt1 = t1press
			oldt2 = t2press
			oldt3 = t3press
			oldt4 = t4press
			t1press = t1press or (k1.value ^ key_invert)
			t2press = t2press or (k2.value ^ key_invert)
			t3press = t3press or (k3.value ^ key_invert)
			t4press = t4press or (k4.value ^ key_invert)

			if oldt1 != t1press or oldt2 != t2press or oldt3 != t3press or oldt4 != t4press:	#If we've added a key since the last loop...
				pix_on = []
				if t1press:
					pix_on.append(3)
				if t2press:
					pix_on.append(2)
				if t3press:
					pix_on.append(1)
				if t4press:
					pix_on.append(0)
				set_neo(pixels, pix_on, color_keypress, False)		#Turn on the neopixels next to the pads.
			time.sleep(0.1)
			timecycles += 1

		if (not t1press) and (not t2press) and (not t3press) and (not t4press) and refresh_needed and not board.DISPLAY.busy:
			#Future: only display if text has changed
			display_strings(magtag.splash, pw_filenames, selected_keynum - (selected_keynum % max_lines_to_show), selected_keynum % max_lines_to_show, max_lines_to_show, font_item)

			display_status(magtag.splash, live_status, font_item)

			board.DISPLAY.show(magtag.splash)
			#while board.DISPLAY.busy:
			#	time.sleep(board.DISPLAY.time_to_refresh + 0.1)
			try:
				board.DISPLAY.refresh()
				refresh_needed = False
			except RuntimeError:					#Refresh too soon, just ignore
				refresh_needed = True

	set_neo(pixels, default_pixels, default_color, True)

	return t1press, t2press, t3press, t4press, timecycles


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


#def delete_files(passfile_dir):
#	"""Deletes all password files from this device."""
#
#	for passnum in range(0, 10000):
#		filename = passfile_dir + pad_zeroes(passnum) + '.pass'
#		if obj_exists(filename) and not isdir(filename):
#			os.remove(filename)


def transform_raw(raw_string, xform_key):
	"""Converts a raw string into a transformed string."""
	#If xform_key empty or false, just return the string as is.
	#If xform_key non-empty, swap the case of all keys lining up with Trues in xform_key (we can think of xform_key being repeated over and over enough to cover the entire raw_string.

	if xform_key:
		output_text = ''
		for s_index, orig_char in enumerate(raw_string):
			#Loop through the xform key values, wrapping around to the 0th element when we get to the end.
			if xform_key[s_index % len(xform_key)]:						#Pull out the True/False value from xform_key
				if orig_char.isupper():
					output_text = output_text + orig_char.lower()
				elif orig_char.isdigit():
					output_text = output_text + str(9 - int(orig_char))	#Replace each digit with 9-thatdigit
				else:
					output_text = output_text + orig_char.upper()
			else:
				output_text = output_text + orig_char
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


def display_strings(screen_h, string_list, starting_index, invert_index, max_strings, font):				# pylint: disable=too-many-arguments
	"""Show (up to) max_strings strings in the string list, starting at index starting_index.
	All lines are black on white except line invert_index which is white on light grey.
	All numbers start at 0.  Use font font."""
	#This assumes a magtag e-ink display (296x128 pixels), and uses the top 4/5 (0-104 out of 128)

	lines_used = 0

	for idx, str_record in enumerate(string_list[starting_index:]):

		if idx == invert_index:
			text_color = e_white
			bg_color = e_lt_grey
		else:
			text_color = e_black
			bg_color = e_white

		this_string = str_record

		out_label = label.Label(
			font,
			x=5,
			y=10 + (idx * 20),
			color = text_color,
			text=this_string[:33] + text_pad,
			line_spacing=0.3,
			background_color=bg_color,
		)
		screen_h.append(out_label)

		lines_used = lines_used + 1
		if lines_used >= max_strings:
			break

	while lines_used < max_strings:
		out_label = label.Label(
			font,
			x=5,
			y=10 + (lines_used * 20),
			color = e_black,
			text=text_pad,
			line_spacing=0.3,
			background_color=e_white,
		)
		screen_h.append(out_label)

		lines_used = lines_used + 1


def display_status(screen_h, status_text, font):
	"""Show the status string at the bottom."""

	line_header = Line(0, 105, 296, 105, color=e_dk_grey)
	screen_h.append(line_header)

	out_label = label.Label(
		font,
		x=5,
		y=115,
		color = e_black,
		text=status_text + text_pad,
		line_spacing=0.0,
		background_color=e_white,
	)
	screen_h.append(out_label)


def load_pw_files(pw_dir):
	"""Load the password files.  Description = filename, actual password = contents."""

	pw_file_list = []
	pw_dictionary = {}

	raw_list = os.listdir(pw_dir)
	for a_file in raw_list:
		if a_file.endswith(".pass"):
			strip_name = a_file.replace(".pass", "")
			pw_file_list.append(strip_name)
			pw_dictionary[strip_name] = load_raw_keyfile(pw_dir, a_file)

	return sorted(pw_file_list), pw_dictionary


def show_error(error_string_array):
	"""Set LEDs red and show error message.  Error message must be an array of strings."""

	set_neo(pixels, [0, 1, 2, 3], red, True)
	display_strings(magtag.splash, error_string_array, 0, 9999, max_lines_to_show, font_item)
	board.DISPLAY.show(magtag.splash)
	while board.DISPLAY.busy:
		time.sleep(board.DISPLAY.time_to_refresh + 0.1)
	try:
		board.DISPLAY.refresh()
	except RuntimeError:
		time.sleep(10)
		board.DISPLAY.refresh()



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

#E-Ink Colors:
e_white = 0xFFFFFF
e_lt_grey = 0x666666
e_dk_grey = 0x999999
e_black = 0x000000
e_transparent = None

max_lines_to_show = 5

text_pad = "                                                                "

#User-editable values
seconds_to_erase = 7
neo_brightness = 0.2

color_keynum = green
color_wakeup = blue
color_keypress = purple
color_blank = black
color_xform_mode = cyan
color_unlock_mode = yellow
color_error = red

no_pass_file_error = [
"No files with the extension",
" .pass were found.  Please",
"create some and reset." ]

no_secrets_error = [
"Credentials and tokens are kept in",
"secrets.py, please add them there!"
]


keyboard = Keyboard(usb_hid.devices)
keyboard_layout = KeyboardLayoutUS(keyboard)

button_status = "NextPg       Up         Down     Select"
unlock_status = "   0             1             2            3"
xform_status =  "                              False       True"

live_status = button_status


#deleteme
#pass_banners = ["Pass 0 78901234567890123456789012", "Pass 1", "Pass 2", "Pass 3", "Pass 4", "Pass 5", "Pass 6"]
#pass_dict = {"Pass 0 78901234567890123456789012": "p0keys", "Pass 1": "p1keys", "Pass 2": "p2keys", "Pass 3": "p3keys", "Pass 4": "p4keys", "Pass 5": "p5keys", "Pass 6": "p6keys"}


#Setup
#if os.uname().machine == 'Adafruit NeoPixel Trinkey M0 with samd21e18':
#	#import touchio								# pylint: disable=import-error
#	#from adafruit_hid.keycode import Keycode				# pylint: disable=import-error,unused-import
#
#	device_type = 0
#	key_invert = False
#
#	pixels = neopixel.NeoPixel(board.NEOPIXEL, 4, brightness=neo_brightness, auto_write=False)
#
#
#	touch1 = touchio.TouchIn(board.TOUCH1)
#	touch2 = touchio.TouchIn(board.TOUCH2)
#el
if os.uname().machine == 'Adafruit MagTag with ESP32S2':
	from adafruit_magtag.magtag import MagTag

	device_type = 1
	key_invert = True							#Magtag keypress .value(s) are inverted; False means pressed, True means released.

	magtag = MagTag()
	magtag.set_background(e_white)

	#pixels = neopixel.NeoPixel(board.NEOPIXEL, 4, brightness=neo_brightness, auto_write=False)
	pixels = magtag.peripherals.neopixels
	magtag.peripherals.neopixel_disable = False

	touch1 = magtag.peripherals.buttons[0]
	touch2 = magtag.peripherals.buttons[1]
	touch3 = magtag.peripherals.buttons[2]
	touch4 = magtag.peripherals.buttons[3]
else:
	print("I don't know how to run on this platform: " + os.uname().machine)
	print("Here are its hardware features: " + str(dir(board)))
	sys.exit(1)

selected_keynum = 0
xform_entry_mode = False
unlock_entry_mode = False
xform_list = []
unlock_list = []
default_color = color_keynum


if obj_exists('/sd/') and isdir('/sd/'):					#Where will the password files be?
	data_dir = '/sd/'							#If this circuitpython board has a microsd slot, the contents of this will show up under /sd/
else:
	data_dir = '/'								#Otherwise, the contents will be immediately at the top of the filesystem.

default_pixels = []

for led in [3, 2, 1, 0]:
	flash_neo(pixels, [led], color_wakeup, 0.5)

font_item = bitmap_font.load_font("fonts/Arial-12.pcf")				#Arial-12 gives 32 characters wide, ~6 lines on the 296x128 character magtag display

refresh_needed = True

pw_filenames = []

try:
	from secrets import secrets
except ImportError:
	show_error(no_secrets_error)
	time.sleep(30)
	raise

if 'unlock' not in secrets:
	secrets['unlock'] = []

pw_filenames, pw_dict = load_pw_files(data_dir)
while not pw_filenames:
	show_error(no_pass_file_error)

	time.sleep(30)
	pw_filenames, pw_dict = load_pw_files(data_dir)


while True:
	#print(str(gc.mem_free()) + " bytes free")				# pylint: disable=no-member
	(t1, t2, t3, t4, cycles) = get_keypress(touch1, touch2, touch3, touch4)

	#print(str(t1) + ' ' + str(t2) + ' ' + str(t3) + ' ' + str(t4) + ' ' + str(cycles))
	#if t1 and t2 and t3 and t4:
	#	if cycles > (seconds_to_erase * 10):
	#	#Note: this program can't delete files while the storage is mounted by the host.  Disable feature for the moment.  Can we use erase_filesystem?  Not sure, as of 6.2.0.
	#		print("Erasing now\n")
	#		#delete_files(data_dir)
	#		storage.erase_filesystem()
	#el
	#if t1 and t2 and t3 and not t4:
	#	if unlock_list == secrets['unlock']:
	#		storage.enable_usb_drive()
	#el
	if t1 and t2:
		#Both Touch1 and Touch2 pressed.  This switches back and forth between normal (select/send keys) mode and enter unlock mode.
		if unlock_entry_mode:
			#Switching back to normal operation
			default_color = color_keynum
			default_pixels = num_to_neo[selected_keynum % 16]
			live_status = button_status
			refresh_needed = True
		elif xform_entry_mode:
			pass
		else:
			#Switching into unlock entry mode
			default_color = color_unlock_mode
			default_pixels = [2, 3]
			live_status = unlock_status
			refresh_needed = True
			unlock_list = []

		set_neo(pixels, default_pixels, default_color, True)
		unlock_entry_mode = unlock_entry_mode ^ True			#xor with true to switch to opposite value (True->False, False->True)

	elif t1:
		#Only T1 pressed.  In normal mode, this moves us to the next screen (+5 passwords).
		if unlock_entry_mode:
			unlock_list.append(0)
			#print(str(unlock_list))
		elif xform_entry_mode:
			pass
		elif unlock_list != secrets['unlock']:
			flash_neo(pixels, [3, 2], color_unlock_mode, 0.5)
		else:
			if selected_keynum == (len(pw_filenames) - 1):
				selected_keynum = 0
			else:
				selected_keynum += 5
				if selected_keynum >= len(pw_filenames):
					selected_keynum = (len(pw_filenames) - 1)

			default_pixels = num_to_neo[selected_keynum % 16]
			set_neo(pixels, default_pixels, color_keynum, True)

			refresh_needed = True
	elif t2:
		#Only T2 pressed.  In normal mode, this moves us to the previous password.
		if unlock_entry_mode:
			unlock_list.append(1)
			#print(str(unlock_list))
		elif xform_entry_mode:
			pass
		elif unlock_list != secrets['unlock']:
			flash_neo(pixels, [3, 2], color_unlock_mode, 0.5)
		else:
			if selected_keynum <= 0:
				selected_keynum = (len(pw_filenames) - 1)
			else:
				selected_keynum -= 1

			default_pixels = num_to_neo[selected_keynum % 16]
			set_neo(pixels, default_pixels, color_keynum, True)

			refresh_needed = True

	elif t3 and t4:
		#Both Touch3 and Touch4 pressed.  This switches back and forth between normal (select/send keys) mode and enter xform mode.
		if xform_entry_mode:
			#Switching back to normal operation
			default_color = color_keynum
			default_pixels = num_to_neo[selected_keynum % 16]
			live_status = button_status
			refresh_needed = True
		else:
			#Switching into xform entry mode
			default_color = color_xform_mode
			default_pixels = [0, 1]
			live_status = xform_status
			refresh_needed = True
			xform_list = []

		set_neo(pixels, default_pixels, default_color, True)
		xform_entry_mode = xform_entry_mode ^ True			#xor with true to switch to opposite value (True->False, False->True)

	elif t3:
		#Only T3 pressed.  In normal mode, this moves us to the next password.  In "enter xform" mode, add a "False/nocasechange" to the xform list.
		if unlock_entry_mode:
			unlock_list.append(2)
			#print(str(unlock_list))
		elif xform_entry_mode:
			xform_list.append(False)
			#print(str(xform_list))
		elif unlock_list != secrets['unlock']:
			flash_neo(pixels, [3, 2], color_unlock_mode, 0.5)
		else:
			if selected_keynum >= (len(pw_filenames) - 1):
				selected_keynum = 0
			else:
				selected_keynum += 1
				if selected_keynum > len(pw_filenames):
					selected_keynum = 0

			default_pixels = num_to_neo[selected_keynum % 16]
			set_neo(pixels, default_pixels, color_keynum, True)

			refresh_needed = True

	elif t4:
		#Only T2 pressed.  In normal mode, send the currently selected password like a keyboard.  In "enter xform" mode, add a "True/casechange" to the xform list.
		if unlock_entry_mode:
			unlock_list.append(3)
			#print(str(unlock_list))
		elif xform_entry_mode:
			xform_list.append(True)
			#print(str(xform_list))
		elif unlock_list != secrets['unlock']:
			flash_neo(pixels, [3, 2], color_unlock_mode, 0.5)
		else:
			#FIXME - use pw_dict instead
			target_string = transform_raw(load_raw_keyfile(data_dir, pw_filenames[selected_keynum] + ".pass"), xform_list)
			if target_string:
				keyboard_layout.write(target_string)

	new_pw_filenames, new_pw_dict = load_pw_files(data_dir)
	if set(new_pw_filenames) != set(pw_filenames):
		pw_filenames = new_pw_filenames
		pw_dict = new_pw_dict

#Future: Make sure we have a successful refresh before sleeping.
magtag.exit_and_deep_sleep(15 * 60)
