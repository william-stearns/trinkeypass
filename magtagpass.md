



## Magtagpass
### Setup
* Install circuitpython 6.2.0 or higher.
* When connected to a USB port, you should have a /Volumes/CIRCUITPY/ mount
* If you don't already have one, create a secrets.py.  Add an 'unlock' key with a line like this:
```
    'unlock': [],
```
* Download Arial-12.pcf to /Volumes/CIRCUITPY/Arial-12.pcf
* Copy the following files and directories (and the directory contents) to /Volumes/CIRCUITPY/lib/:

adafruit_magtag/
adafruit_portalbase/
adafruit_bitmap_font/
adafruit_display_text/
adafruit_display_shapes/
adafruit_hid/
adafruit_io/
adafruit_requests.mpy
adafruit_fakerequests.mpy
adafruit_miniqr.mpy
neopixel.mpy
simpleio.mpy

* Create a sample password file /Volumes/CIRCUITPY/00_sample.pass with the following content:
```
#This is a sample password.
```


* Copy magtagpass.py to /Volumes/CIRCUITPY/code.py .

### Use
* Press "Select" to send the contents of the first password file over the USB cable to the connected computer, and those keys will be typed as if you typed them.
