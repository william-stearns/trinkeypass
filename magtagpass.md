



## Magtagpass

### Overview

   The code here, when paired with an Adafruit Magtag, provides a
hardware password safe.  Passwords are stored away from your main systems
and are fed on request to the system connected by a USB cable (as if
they'd been typed on a normal USB keyboard).


### Setup

* Install circuitpython 6.2.0 or higher.  See any of the Adafruit Magtag
setup guides for the steps.

* When connected to a USB port, you should have a /Volumes/CIRCUITPY/
mount.

* If you don't already have one, create a secrets.py.  Add an 'unlock'
key with a line like this:
```
    'unlock': [],
```

* Download Arial-12.pcf to /Volumes/CIRCUITPY/fonts/Arial-12.pcf .  If
you click the "Download project bundle" link on
<https://learn.adafruit.com/magtag-covid-tracking-project-iot-display/project-code>
, the zip file you get contains three sizes of Arial fonts.

* Copy the following files and directories (and the directory contents)
to /Volumes/CIRCUITPY/lib/:

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

* Create a sample password file /Volumes/CIRCUITPY/00_sample.pass with
the following content:
```
#This is a sample password.
```

* Copy magtagpass.py to /Volumes/CIRCUITPY/code.py .

### Use

* Press "Select" to send the contents of the first password file over the
USB cable to the connected computer, and those keys will be typed as if
you typed them.

* Once you add more password files (which need a ".pass" extension),
you'll be able to move up and down through the files with the Up and Down
buttons.  Note that the descriptions on the screen match the filenames
you use.


### Lock and unlock
   To require the user to enter an unlock code before using any passwords:

* Set a code by editing /Volumes/CIRCUITPY/secrets.py .  Modify the
'unlock':... line and add the digits the user must enter:
```
    'unlock': [0, 1, 2, 3],
```

* If the magtag doesn't automatically reboot when the file is saved, tap
the Reset button on the back.

* At first boot, enter unlock mode by pressing the left 2 buttons (D15
and D14) at the same time.

* The banner line on the bottom will change to "0    1    2    3".  Press
the button below 0, then the button below 1, then 2 and 3.

* Press the left 2 buttons simultaneously again to finish entering the
unlock code.

* Now you should be able to use "Select" to feed passwords normally.

* To lock the unit, press the left 2 buttons at the same time, release,
(wait for the screen to update) then press them both again and release. 
This is effectively entering a new - incorrect - unlock code, locking the
unit.




