"""This code, designed to run on an Adafruit Neo Trinkey, sends a password
to the connected system as if it was a keyboard."""
import os
import sys
import time
import board														
import touchio														
import usb_hid														
import neopixel														
import storage														
from adafruit_hid.keyboard import Keyboard										
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS								
#from adafruit_hid.keycode import Keycode										
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
	while (not t1press) and (not t2press):							
		while (k1.value ^ key_invert) or (k2.value ^ key_invert):			
			oldt1 = t1press
			oldt2 = t2press
			t1press = t1press or (k1.value ^ key_invert)
			t2press = t2press or (k2.value ^ key_invert)
			if oldt1 != t1press or oldt2 != t2press:				
				if t1press and t2press:
					set_neo(pixels, [1, 2], color_keypress, False)		
				elif t1press:
					set_neo(pixels, [2], color_keypress, False)		
				elif t2press:
					set_neo(pixels, [1], color_keypress, False)		
			time.sleep(0.1)
			timecycles += 1
	set_neo(pixels, default_pixels, default_color, True)
	return t1press, t2press, timecycles
def load_file_into_string(filename):
	"""Reads the entire contents of a file into the returned string.  First returned object is string form, second is raw bytes."""
	file_string = None
	raw_bytes = None
	if obj_exists(filename) and not isdir(filename):				
		with open(filename, 'rb') as read_h:
			raw_bytes = read_h.read()
			file_string = str(raw_bytes, 'ascii')
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
#	
#	
#			
#			if xform_key[s_index % len(xform_key)]:						
#					output_text = output_text + str(9 - int(orig_char))	
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
num_to_neo = [ [], [0], [1], [0,1], [2], [0,2], [1,2], [0,1,2], [3], [0,3], [1,3], [0,1,3], [2,3], [0,2,3], [1,2,3], [0,1,2,3] ]	
red = (32, 0, 0)
green = (0, 32, 0)
blue = (0, 0, 32)
cyan = (0, 32, 32)
purple = (32, 0, 32)
yellow = (32, 32, 0)
white = (32, 32, 32)
black = (0, 0, 0)
zero_pads = '0000'
seconds_to_erase = 7
max_unlock_failures = 7
neo_brightness = 0.2
color_keynum = green
color_wakeup = blue
color_keypress = purple
color_blank = black
color_unlock_mode = yellow
color_error = red
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
unlock_entry_mode = False
unlock_code = ""
unlock_failures = 0
default_color = color_keynum
if obj_exists('/sd/') and isdir('/sd/'):					
	data_dir = '/sd/'							
else:
	data_dir = '/'								
pw_subdir = ''									
default_pixels = []
for led in [0, 1, 2, 3]:
	flash_neo(pixels, [led], color_wakeup, 1)
while True:
	(t1, t2, cycles) = get_keypress(touch1, touch2)
	if t1 and t2:
		if cycles >= (seconds_to_erase * 10):
			storage.erase_filesystem()
		#	
		elif unlock_entry_mode:
			default_color = color_keynum
			default_pixels = num_to_neo[selected_keynum % 16]
			if not obj_exists(data_dir + unlock_code) or not isdir(data_dir + unlock_code):
				unlock_failures += 1
				if unlock_failures > max_unlock_failures:
					storage.erase_filesystem()
			elif obj_exists(data_dir + unlock_code) and isdir(data_dir + unlock_code):		
				pw_subdir = unlock_code + '/'
				selected_keynum = 0
				default_pixels = num_to_neo[selected_keynum % 16]
				if unlock_code:
					unlock_failures = 0
		else:
			default_color = color_unlock_mode
			default_pixels = [0,3]
			unlock_code = ""
		set_neo(pixels, default_pixels, default_color, True)
		unlock_entry_mode = unlock_entry_mode ^ True			
	elif t1:
		if unlock_entry_mode:
			unlock_code = unlock_code + '1'
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
		if unlock_entry_mode:
			unlock_code = unlock_code + '2'
		else:
			target_string = load_raw_keyfile(data_dir + pw_subdir, (zero_pads + str(selected_keynum))[-4:] + '.txt')
			if target_string:
				keyboard_layout.write(target_string)
