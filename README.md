# trinkeypass
Adafruit Neo Trinkey password safe

## Intro

   Password managers and keys do a good job of authenticating us, but
each has at least one passphrase for authentication.  I find I need a
physical store for these especially sensitive passwords, passphrases, and
pins.  For that, we have the TrinKeyPass - the world's smallest password
vault.



## Quickstart

### Initial setup

1. Buy an Adafruit Neo Trinkey (<https://adafru.it/4870> , redirects to
<https://www.adafruit.com/product/4870> $6.95 ea., bulk discounts
available).  Better yet, buy 2 so you have a backup.

2. These have USB-A connectors.  If you're looking to connect them to
other USB connectors or a lightning connector, pease see Other Resources
at the end.

3. Download the firmware from <https://adafru.it/RD7> , redirects to
<https://circuitpython.org/board/neopixel_trinkey_m0/> .  You need the
most recent 7.x UF2 file, which will download with a filename like
adafruit-circuitpython-neopixel_trinkey_m0-en_US-7.0.0-alpha.2.uf2 .
<https://adafruit-circuit-python.s3.amazonaws.com/bin/neopixel_trinkey_m0/en_US/adafruit-circuitpython-neopixel_trinkey_m0-en_US-7.0.0-alpha.2.uf2>
as of this writing.

4. Insert the Trinkey into a USB port.  On a Mac - and possibly other
platforms too - the OS may note that a new keyboad and/or drive have been
inserted.  Feel free to dismiss any windows asking you to identify the
keyboard.  If you're asked if you want to automatically mount the drive,
I'd suggest Yes while you're going through this initial setup, then
change that to No when you're finished adding passwords.

5. Tap the black reset button in the middle of the board **twice**.  The
4 LEDs will turn green and the storage on the Trinkey will be
automatically mounted (under /Volumes/TRINKEYBOOT/ on a Mac.)

6. Copy the .UF2 file into this directory.  All the LEDs will turn red,
that drive will automatically disconnect (and put up a harmless warning
that it disconnected without unmounting first).  After a few seconds it
will mount the real storage you need (on /Volumes/CIRCUITPY/ on a Mac).

7. "code.py" is trinkeypass.py with comments removed.  Download code.py from
https://raw.githubusercontent.com/william-stearns/trinkeypass/main/code.py
, place it in this directory, and name it code.py.  Here's the command to
do it:

```
cd /Volumes/CIRCUITPY/
curl -fsSL https://raw.githubusercontent.com/william-stearns/trinkeypass/main/code.py -o code.py
touch .metadata_never_index
sync
```

8. If you don't already have any password files (like 0000.txt and
0001.txt), create 2 test "password" files for Trinkey to use:

```
cd /Volumes/CIRCUITPY/
echo "This is a test password in 0000.txt." >>0000.txt
echo "And here's another one in 0001.txt" >>0001.txt
sync
```




### Trinkeypass components

1. You've already used the reset button, the black button between the
LEDs and the largest chip.  If anything goes weird, tap it once to
restart the password safe software.

2. There are 4 LEDs numbered 0-3.  LED 0 is next to the reset button. 
LEDs 1-3 are clockwise from LED 0.  When the trinkeypass software starts,
it flashes the 4 LEDs in order in blue.

3. There are two touch-sensitive pads, T1 and T2, at the far end from the
USB connector.  You'll tap one or both of these to get the Trinkey to do
something.  T2 is on the same edge as the reset button, T1 on the
opposite edge.  (The board has a "1" and a "2" silkscreened as reminders
next to the pads and the outermost LEDs.)



### Using the password feature

1. Click your mouse in a window where you can enter some text.  This can
be a graphical application (notepad/gedit) or a text window/terminal.  To
see what's returned without any chance of actually doing something, run
the command `cat >/dev/null` to show and discard all keys.

2. Press button T2 (the one on the same edge as the reset key).  This
will send the contents of 0000.txt to your computer as if you'd typed
those characters by hand on a USB keyboard.  The blue light next to the
keypad will flash to show you the button worked.  Try it a few more
times.

3. Now switch to the next password.  To do this, press button T1 - the
LED next to it will flash briefly.  Now LED 0 will light green to
indicate we're on a different key.  Press T2 and password *0001* will
come out into your selected window as if you typed it on a USB keyboard.

4. If you press T1 again, this would move to the third key (in 0002.txt,
if you had one).  Since you don't, it will go back to the beginning of
the list, 0000.txt .  Press T2 to confirm you're back on the first
password.

5. The LEDs show you which key is selected.  Look at all the LEDs that
are green and add up their values:

* LED0 (next to the reset button) has a value of 1
* LED1 (between LED0 and T2) has a value of 2
* LED2 (next to T1) has a value of 4
* LED3 has a value of 8

   Add up the values for each LED that's lit; the sum is the number of
the key you're using.  That's why all LEDs are off when you're on Key
0000.txt at start.  When you switch to the second key (0001.txt), LED0
lights and all the rest are off.

   When you get to the 17th password (0016.txt), the LEDs start back at
all black since there are only 4 of them.  Similarly, when you get to the
33rd password (0032.txt), they'll go back to black again.



## Adding or editing passwords

1. You can add more passwords or edit them at any time.  Each one goes in
its own file starting with 0000.txt, 0001.txt, 0002.txt, etc.  

2. Everything you place in the file is sent verbatim, so if you want a
linefeed at the end of a password to automatically submit it, make sure
you have a linefeed in the file.  If you want to just have the password
keys entered but want to manually edit them before pressing enter, leave
off the linefeed.

3. As soon as you save the file (and run the command `sync` on MacOS or
Linux to make sure the changes are saved), the new password is ready to
use.  You don't have to restart or reinsert the key.

4. The password files are named 0000.txt through 9999.txt, so you can
have up to 10,000 of them (though you'll run out of storage to hold those
files before then).


### Actually using this to enter passwords

1. Save a real password/passphrase/pin to 0001.txt .  Press T1 until just
LED0 is lit, indicating that you're on the 2nd password, 0001.txt .

2. Start logging in; stop when you get to the password/passphrase/pin
field.

3. Make sure your cursor is in the password/passphrase/pin box or window.

4. Press T2 to type the characters from 0001.txt .  If that file ends in
a linefeed, the "Enter" key will be pressed and the password will be
automatically submitted.



## Tips and tricks

* If the key is loose in your USB port, place a folded post-it note under
it (the side *away* from the USB contact pins) before inserting it into
the USB port.

* This system can store and type any printable characters from your
keyboard.  This includes passwords, passphrases, pins, keys, and long
blocks of text you commonly use ("Thank you for writing in with your
computer issue.  Have you tried rebooting it?  --Tech support").

* Use 0000.txt to store contact information, including "How to return
this to me" information should someone find it.

* In 0001.txt place hints of what's stored in the other slots, like:

```
2  Password safe
3  Home email
4  Work email
...
```

   If you forget what they are, go back to this slot 1 and press T2 to
have the hints come out in whatever window has keyboard focus.

* Since this device can only give the barest of feedback of which key
you're on (the LEDs that indicate 0-15, and wrap around when they reach
any multiple of 16), you might want to use a standard password vault like
lastpass and reserve this for master passwords and key passphrases -
things you wouldn't normally want to place in a vault.

* You can also use this drive to store key files, but we discourage
placing all factors needed to login on any single storage device
including this one.

* At the time of this writing (Apr 2021), it appears that circuitpython
may only support the US keyboard layout.  The authors are open to other
layouts.  For more info, see 
<https://github.com/adafruit/Adafruit_CircuitPython_HID/blob/master/adafruit_hid/keyboard_layout_us.py>

* You don't have to put the entire password in here.  If you have a way
to mentally generate, say, the first 5 characters of a password based on
the hostname, type those into the password box by hand and enter the
*remaining* letters that are stored in Trinkeypass.  Just remember that
the characters you type plus the characters provided by trinkeypass need
to end up the same as what the remote system/application expect.

* You could even split any given password between two trinkeys held by
two different people for a particularly sensitive password.

* It's a good idea to buy 2 or more of these and load your passwords on
all of them.  You can keep one with you, perhaps in a wallet or on a
keyring, and place the others in safe locations.

* This approach could be very handy for systems that are managed by
multiple people.  A Trinkeypass could hold a root/Administrator password,
database credentials, and any other credentials not needed in normal
operation.  This could be passed from admin to admin on shift changes or
stored in a central locked area.

* To load an ssh private key into memory, put the following into one of
your password files.  The key won't be saved on disk, but be aware that
the content may be viewable by someone that looks at the list of running
processes at the right moment.  Everything between the double quotes is
your private key.

```
echo "-----BEGIN RSA PRIVATE KEY-----
MIIJJ...........
...
-----END RSA PRIVATE KEY-----" | ssh-add -
```

   Go to a command prompt on a system running the ssh-agent.  Feed these
characters into the shell and the key will be loaded into the ssh-agent.

* You can enter more than one field on a web form.  Simply put your
username on the first line and put the password on the second line, both
ending in a linefeed.  Both will be entered.  (That's not as safe as now
an attacker knows what account you have, but it's more convenient.)

* If you hold down both T1 and T2 for longer than 7 seconds, everything
on the unit is erased.

* Also, if you try to switch to a different password collection more than
7 times (see below), everything on the unit is erased too.


### Unlocking alternate password collections

   By default, trinkeypass gets its passwords from files in the top level
directory named 0000.txt, 0001.txt, and so on.  By creating directories
on the drive you can store alternate collections of password files and
switch between them.

1. Create a directory called "1212" under /Volumes/CIRCUITPY/ .  In
/Volumes/CIRCUITPY/1212/ , place a file called 0000.txt that has a
_different_ password than the one immediately inside /Volumes/CIRCUITPY/
.  Now create another file in the same directory called 0001.txt .

2. To switch to this collection, press T1 and T2 at the same time to
enter "unlock" mode (note that two LEDs turn yellow).  Since the
directory you want to use is named "1212", press T1, T2, T1, and finally
T2.  Now press T1 and T2 at the same time again to show you're done. 
You've now switched to the new passwords.

3. Press T2 to push out the current password.  Note that it's the one
inside /Volumes/CIRCUITPY/1212/0000.txt , not the one in
/Volumes/CIRCUITPY/0000.txt .

4. To switch back to the top level directory, press T1 and T2, release
them, and press both again and release.

5. You can have multiple directories like this, just name them with 1s
and 2s and include at least one password file 0000.txt in each.  Now you
can break up your passwords into collections like:
* Home
* Master passwords
* Production
* SSH
* Test

6. Please make your directory names long so they're not easily guessed.

7. Note that when the Trinkeypass first starts up it will feed out text
from the files in /Volumes/CIRCUITPY/ without requiring you to enter any
unlock code).  Because of this you may want to put dummy text in these
files and put your real passwords in the subdirectories.  Example:
```
#Please return this to Bob Jones, 1 Main St, Springfield IL and I will mail you a $20 reward.
```


### Using the lockdown feature.

   The Trinkey shares a drive that mounts on /Volumes/CIRCUITPY/ , which
is exactly what you want when you want to update the code or edit any
password files.  This is not what you want forever because this makes the
files visible to any person or program on the computer.

   Once you're happy with the configuration and you no longer want to
make any changes, you can totally lock down the system (which will no
longer share the drive on which your unlock code and passwords are
stored, as well as removing a few other features that might potentially
give an attacker access).  Make sure you've entered an unlock pin first,
then:

1. Go to /Volumes/CIRCUITPY/

2. Rename bootlockdown.py to boot.py

3. Run "sync" and wait two seconds.

4. Press Reset on top of the Trinkey.

   From this point on the drive will no longer be visible.  There is no
way to return to normal operation.





## Risks

* Note that if the system into which you've inserted the Trinkeypass is
running a keyboard sniffer, that program will see the injected password
just as easily as a password typed at an actual keyboard.

* We discourage indexing or backing up this drive.

* If you're using multiple factors to log in somewhere (such as a 
password, an ssh key, and the passphrase to unlock that ssh key, please
do not store all factors in any single place (including on this Trinkey).


---
## Other resources

* Adafruit document describing the Neo Trinkey:
<https://learn.adafruit.com/adafruit-neo-trinkey>

* I've done tests on MacOS, Linux, and Windows 10 with success on all 3. 
I've tried web logins, ssh key loading, sudo password entry, and password
login over ssh.  This password entry should work anywhere you can type
keystrokes with a normal keyboard.

* To plug this into a USB-C port: USB-A -> USB-C adaptor
(<https://www.amazon.com/gp/product/B086WFD4V6/>, $4.99 for a 4-pack). 

* To plug this into a microusb port:
(<https://www.amazon.com/UGREEN-Adapter-Samsung-Controller-Android/dp/B00N9S9Z0G/>,
$7 for a 2-pack)

* To plug this into a lightning port used on many iphones and ipads: the
Lightning to USB Camera adapter
(<https://www.amazon.com/Apple-Lightning-USB3-Camera-Adapter/dp/B01F7KJDIM/>
from Apple, $35, supports USB3, or
<https://www.amazon.com/Adapter-Charging-Portable-Compatible-Support/dp/B08LQ2K8RL/>,
generic, USB2 only, $13)
    Note: my early tests with these have been unsuccessful.


* To hook it to a keychain, order some small keychain rings like
(<https://www.amazon.com/gp/product/B01MG68TV6/> , $6.96 for a 200-pack)
